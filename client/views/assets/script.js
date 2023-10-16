let chats;
let id;
let noti;
let isHidden = true;
let socket;

let eel;

async function hidden(state) {
    isHidden = state;
    return isHidden;
}
// Exposing functions to eel
try {
    eel.expose("toTray");
    function toTray() {
        socket.close();
        try {
            eel.to_tray();
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

let init = () => {
    try {
        eel.get_server_ip().then((ip) => {
            eel.log("Connecting to server " + ip);
            socket = io(`http://${ip}:51998`);

            // LISTENERS
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

            // Get chat history
            socket.emit("command", "history", (e) => {
                showMessages(e);
            });
        });
    } catch ({ name, msg }) {
        if (name == "ReferenceError") {
            console.log(`No eel, You're fucked`);
        }
    }
    noti = document.querySelector("#show_notif");
    chats = document.querySelector("#chats");

    let username = sessionStorage.getItem("username");
    document.querySelector("#inp_name").innerHTML = username;
    document.querySelector("#input input").addEventListener("keypress", (e) => {
        if (e.key == "Enter" && e.shiftKey) {
            e.target.value += "\\n";
        } else if (e.key == "Enter") {
            let text = e.target.value;
            e.target.value = "";
            socket.emit("message", {
                text: text,
                name: username,
            });
        }
    });
}; // Close onload

function showMessages(msgs) {
    for (let i of msgs) {
        let child = document.createElement("div");
        child.innerHTML =
            "<p>" +
            `<span>${i.name} - ${i.from}</span>` +
            htmlEnc(`${i.text}`) +
            "</p>";
        chats.append(child);
        child.classList.add("message");
        if (id == i.name) {
            child.classList.add("me");
        }
    }
    let froms = msgs.map((msg) => msg.name).join(', ');
    notify("New Messages", `from ${froms.substring(0, 15)}...`);
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
    try {
        eel.send_notify(text);
    } catch ({ name, msg }) {
        if (name == "ReferenceError") {
            console.log(`Notification ${text}`);
        }
    }
}

window.addEventListener("pywebviewready", function () {
    console.log("ready");
    eel = pywebview.api;
    init();
});
