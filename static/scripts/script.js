const token = document.getElementById("token")
const channel = document.getElementById("channel")
const message = document.getElementById("message")
const warn = document.getElementById("warn")
const btn = document.getElementById("btn")

btn.onclick = function() {
    fetch(`/send?token=${token.value}&channelid=${channel.value}&message=${message.value}`)
        .then(function(respond) {
            return respond.text()
            .then(function(data) {
                if (data==="Success") {
                    warn.classList.add("success")
                    warn.classList.remove("warn")
                    warn.innerHTML = "Success!"
                    setTimeout(function() {
                        warn.classList.remove("success")
                        warn.classList.add("warn")
                    }, 5000)
                } else {
                    warn.classList.add("error")
                    warn.classList.remove("warn")
                    warn.innerHTML = "Error!"
                    setTimeout(function() {
                        warn.classList.remove("error")
                        warn.classList.add("warn")
                    }, 5000)
                }
            })
        })
}