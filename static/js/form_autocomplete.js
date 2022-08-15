async function updateSelectField(fieldToUpdate, value, fieldToEmpty) {
    formElement = fieldToUpdate.closest('form')
    const data = new URLSearchParams(new FormData(formElement));

    console.log(formElement.action)
    response = await fetch(formElement.action, {
        method: "post",
        body: data
    })

    html = await response.text()
    const parser = new DOMParser();
    const htmlDocument = parser.parseFromString(html, "text/html");
    const formContent = htmlDocument.documentElement.querySelector("form")

    formElement.replaceWith(formContent)

    initEvent()
    /* // Empty and disable form field
    for (f of fieldToEmpty) {
        [...f.options].forEach(element => {
            element.remove()
        });

        f.disabled = true
    }    

    // Update needed field with value form json endpoint
    for (opt of options) {
        // first elem in array is DisplayName, second is IRI
        fieldToUpdate.add(new Option(opt[1], opt[0]))
    }        
    fieldToUpdate.disabled = false*/
}

function initEvent() {
    var select1 = document.querySelector("#{{ form.query1.id }}")
    var select2 = document.querySelector("#{{ form.query2.id }}")
    var select3 = document.querySelector("#{{ form.query3.id }}")

    select1.addEventListener('change', () => {
        updateSelectField(select2, select1.value, [select3])
    })

    select2.addEventListener('change', () => {
        updateSelectField(select3, select2.value, [])
    })
}

initEvent()


