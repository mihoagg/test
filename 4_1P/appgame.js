const app = Vue.createApp({
        data() {
            return{
                message: 'start guessing',
                min: 1,
                max: 100,
                numberToGuess: 0,
                userGuess: null,
                userGuess: ''
            }
        },
        methods: {
        handleClick() {
            this.message = `You guessed: ${this.userGuess}`;
        },
        generateRandomNumber() {
            this.numberToGuess = Math.floor(Math.random() * this.max) + this.min;
        },

        checkGuess() {
            if (userGuess == numberToGuess) {
                this.message = `You got it!`
            }
            else if (userGuess < numberToGuess) {
                this.message = `Guess higher`
            }
            else {
                this.message = `Guess lower`
            }
        },
        mounted() {
            numberToGuess = this.generateRandomNumber();
            console.log(numberToGuess);
        }
    }
    });
app.mount('#app')