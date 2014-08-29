/* http://mitadmissions.org/discover/majors */

let descriptions = []
let rows = document.getElementById("majors").querySelectorAll("tr > td > a");
for (let i = 0; i < rows.length; i++) {
    let description = rows[i].text.trim();
    if (description != "")
        descriptions.push(description);
}

let rows = document.getElementById("majors").querySelectorAll("td:first-child + td");
let majors = [];
for (let i = 1; i < rows.length; i++) {
    let number = rows[i].textContent.trim();
    majors.push(number + ";" + descriptions[i-1]);
}

majors.join("\n");
