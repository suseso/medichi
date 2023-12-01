const url = "https://v2.jokeapi.dev/joke/Any?lang=es"
let app = new Vue({
    el: '#Jokes',
    data: {
        joke: {}
    },
    created() {
        fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            this.info = data;
            if(this.info.type == 'single')
                this.joke = data.joke;
            else
                this.joke = data.setup + " ==> " + data.delivery
        })
        .catch(error => console.log(error));
    }
})