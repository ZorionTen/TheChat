let chats;
let id;
let noti;
let isHidden = false;
let socket;
try {
    eel.expose("toTray");
    function toTray() {
        socket.close()
        try {
            eel.resize(0, 0);
            isHidden = true;
            eel.log("Hidden");
        } catch (e) {
            console.log(e);
            return "error";
        }
    }
    eel.expose("fromTray");
    function fromTray() {
        try {
            isHidden = false;
            window.resizeTo(1600, 800);
        } catch (e) {
            return "error";
        }
        return 12;
    }
} catch ({ name, msg }) {
    if (name == "ReferenceError") {
        console.log(`No eel, not exposed`);
    }
}

onload = () => {
    noti = document.querySelector("#show_notif");
    socket = io("http://0.0.0.0:51998");
    socket.on("message", function (data) {
        showMessages(data);
    });

    socket.on("command", (data) => {
        if (data.hasOwnProperty("data")) {
            if (data.data.hasOwnProperty("ip")) {
                id = data.data.ip;
            } else if (data.data.hasOwnProperty("members")) {
                let mems = document.querySelector("#mems");
                mems.innerHTML = "";
                for (let i of data.data.members) {
                    mems.innerHTML += `<span>${i}</span>`;
                }
            }
        }
    });

    chats = document.querySelector("#chats");
    socket.emit("command", "history", (e) => {
        showMessages(e);
    });

    document.querySelector("#input input").addEventListener("keypress", (e) => {
        if (e.key == "Enter" && e.shiftKey) {
            e.target.value += "\\n";
        } else if (e.key == "Enter") {
            let text = e.target.value;
            e.target.value = "";
            socket.emit("message", {
                text: text,
                name: document.querySelector("#inp_name").value,
            });
        }
    });

    document.querySelector("body").addEventListener("onunload", () => {
        eel.log("Closing");
        socket.close();
    });

}; // Close onload

function showMessages(msgs) {
    for (let i of msgs) {
        let child = document.createElement("div");
        child.innerHTML =
            "<p>" +
            `<span>${i.s_name || i.name} - ${i.from}</span>` +
            htmlEnc(`${i.text}`) +
            "</p>";
        chats.append(child);
        child.classList.add("message");
        if (id == i.from) {
            child.classList.add("me");
        }
    }
    notify("THE CHAT", "New Messages");
    toBottom();
}

function htmlEnc(s) {
    let new_txt = s
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/'/g, "&#39;")
        .replace(/"/g, "&#34;")
        .replace("\\n", "<br>");
    return new_txt;
}

function toBottom() {
    chats.scrollTo(0, chats.scrollHeight);
}

function notify(title, text) {
    if (!document.hasFocus() || !isHidden) {
        return false;
    }
    try {
        eel.send_notify(text);
    } catch ({ name, msg }) {
        if (name == "ReferenceError") {
            console.log(`Notification ${text}`);
        }
    }
}
