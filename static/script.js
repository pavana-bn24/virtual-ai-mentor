async function sendMessage() {

    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (!message) return;

    // Hide hero card after first message
    const hero = document.getElementById("hero-card");

    if(hero){
        hero.style.display = "none";
    }

    const chat = document.getElementById("chat-box");

    chat.innerHTML += `
        <div class="user">
            ${message}
        </div>
    `;

    input.value = "";

    chat.innerHTML += `
        <div class="typing" id="typing">
            🤖 AI Mentor is thinking...
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        const typing = document.getElementById("typing");

        if(typing){
            typing.remove();
        }

        chat.innerHTML += `
            <div class="bot">
                ${data.response}
            </div>
        `;

    }
    catch(error){

        const typing = document.getElementById("typing");

        if(typing){
            typing.remove();
        }

        chat.innerHTML += `
            <div class="bot">
                ⚠️ AI Mentor is currently unavailable.
            </div>
        `;
    }

    chat.scrollTop = chat.scrollHeight;
}

function clearChat(){

    document.getElementById("chat-box").innerHTML = "";

    const hero = document.getElementById("hero-card");

    hero.style.display = "block";
}

document
.getElementById("user-input")
.addEventListener("keypress", function(e){

    if(e.key === "Enter"){
        sendMessage();
    }

});