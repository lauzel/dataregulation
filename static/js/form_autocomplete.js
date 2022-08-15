class FormAutoUpdate {
    constructor(selector) {
        let formElement = document.querySelector(selector)
        this.form = formElement

        this.initEvent()
    }

    initEvent() {
        let selects = this.form.querySelectorAll("select")
        let self = this

        selects.forEach((s) => {
            s.addEventListener('change', (e) => {
                self.updateForm(e)
            })
        })
    }

    async updateForm(event) {
        let formElement = this.form
        const data = new URLSearchParams(new FormData(formElement));

        let response = await fetch(formElement.action, {
            method: "post",
            body: data
        })

        let html = await response.text()
        const parser = new DOMParser();
        const htmlDocument = parser.parseFromString(html, "text/html");
        const formContent = htmlDocument.documentElement.querySelector("form")

        formElement.replaceWith(formContent)

        this.form = formContent
        this.initEvent()
    }
}
