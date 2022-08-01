
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');

  //create root
  const root1 = ReactDOM.createRoot(document.getElementById("emails-view-content"));
  const root2 = ReactDOM.createRoot(document.getElementById("email-des"));


function compose_email(mail) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-des').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  let [subject, body, sender] = Array(3).fill("");
  if(mail.id) {
    subject = `Re: ${mail.subject}`;
    if(mail.subject.startsWith('Re:')) subject = mail.subject;

    body = `On ${mail.timestamp} ${mail.sender} wrote: \r\n ${mail.body} \r\n Reply: `
    sender = mail.sender;
  }
  // Clear out composition fields
  


  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-des').style.display = 'none';

  //Load the emails
  load_emails(mailbox);

  // Show the mailbox name
  document.querySelector('#emails-view-title').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function send_email(event) {
  event.preventDefault();
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.getElementById("compose-recipients").value,
        subject: document.getElementById("compose-subject").value,
        body: document.getElementById("compose-body").value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });
}

function load_emails(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      
      
      root1.render(<MailList mails={emails} />)

      // ... do something else with emails ...
  });
}


function MailList(props) {
  const emails = props.mails;
  const mailItem = emails.map((email) =>
  <div key={email.id.toString()} className={`row border border-dark rounded p-3 mb-1 text-monospace row ${email.read ? 'bg-light' : 'bg-white'}`} onClick={() => {show_email(email.id)}}>
        <div className="col-2 fw-bold">
                   {email.sender}
           </div>
         <div className="col">{email.subject}</div>
         <div className="col-2 text-end">{email.timestamp}</div>
        </div>
  );
  return (
    <div>{mailItem}</div>
  );
}

function show_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-des').style.display = 'block';

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print emails
      console.log(email);
      root2.render(<Mail mail={email} />)
      // ... do something else with emails ...
  });
}

function Mail(props) {
  let mail = props.mail;
  let recipient = mail.recipients[0];
  let len = mail.recipients.length;
  for (let i = 1; i < len; i++) {
    recipient += `, ${mail.recipients[i]}`;
  }
  let state = true;
  if(mail.archived) state = false;
 
  return (
  <div className="p-3">
    <div className="head m-2 p-3 bg-light">
      <div><b>From:</b> {mail.sender}</div>
      <div><b>To:</b> {recipient}</div>
      <div><b>Subject:</b> {mail.subject}</div>
      <div><b>Timestamp:</b> {mail.timestamp}</div>
    </div>
    <div className="row m-2">
        <div className="col-2 p-1">
          <button className="bg-primary text-white border rounded" onClick={() => compose_email(mail)}>Reply</button>
        </div>
        <div className="col"></div>
        <div className="col-2 p-1 text-end">
          <button className="bg-primary text-white border rounded" onClick={() => archive_mail(mail.id, state)}>{state ? "Archive" : "Unarchive"}</button>
        </div>
      </div>
    <div className="body bg-light m-2 p-3">
      <div>
        {mail.body}
      </div>
    </div>
  </div>
  );
}

function archive_mail(id, state) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: state
    })
  })
  location.reload();
}
