text = document.getElementsByTagName('textarea')[0];


highlight = [{name: "bold", format: "****", len : 2, dis: "<b>B</b>"},
            {name: "italic", format: "**", len : 1, dis: "<i>I</i>"},
            {name: "strike", format: "~~~~", len : 2, dis: "<s>Strike</s>"},
            {name: "sub", format: "<sub></sub>", len : 5, dis: "<sub>Sub</sub>"},
            {name: "sup", format: "<sup></sup>", len : 5, dis: "<sup>Sup</sup>"},
            {name: "h1", format: "#", len : 1, dis: "<b>H1</b>"},
            {name: "h2", format: "##", len : 2, dis: "<b>H2</b>"},
            {name: "h3", format: "###", len : 3, dis: "<b>H3</b>"},
            {name: "h4", format: "####", len : 4, dis: "<b>H4</b>"},
            {name: "h5", format: "#####", len : 5, dis: "<b>H5</b>"},
            {name: "h6", format: "######", len : 6, dis: "<b>H6</b>"},
            {name: "quote", format: ">", len : 1, dis: "Quote"},
            {name: "code", format: "``", len : 1, dis: "Code"},
            {name: "link", format: "[link text here](link address here)", len : 15, dis: "Link"},
];

for (let each of highlight)
{
    let el = document.getElementsByClassName("tools")[0];
    el.innerHTML += '<button type="button" id=' + each["name"] + '>' + each["dis"] + '</button>';

}

for (let each of highlight)
{
    let element = document.getElementById(each["name"])
        element.onclick = function(){
            let end = text.selectionEnd;
            let start = text.selectionStart;
            text.value = text.value.substring(0, start) + each["format"] + text.value.substring(end);
            text.focus();
            text.selectionEnd= end + each["len"];
        }
}