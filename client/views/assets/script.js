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

            socket.emit("command", "history", (e) => {
                showMessages(e);
            });
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

            socket.on("edited", (data) => {
                document.querySelector(
                    `span[data-id="${data.uid}"]`
                ).innerHTML = data.text;
            });

            socket.on("deleted", (data) => {
                document
                    .querySelector(`p[data-id="${data.uid}"]`)
                    .parentElement.remove();
            });

            document.querySelector('#input').addEventListener('transitionend',(e)=>{
                toBottom();
            })

            checkUpdate();
            setInterval(checkUpdate, 12 * 3600000);
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
    document
        .querySelector("#input textarea")
        .addEventListener("keypress", (e) => {
            if (e.key == "Enter" && !e.shiftKey) {
                e.preventDefault();
                let text = e.target.value;
                let reply_to = "";
                try {
                    reply_to = document.querySelector("#quote .uid").innerHTML;
                } catch {}
                if (text.length < 1) {
                    return true;
                }
                e.target.value = "";
                clearQuote();
                socket.emit("message", {
                    text: text,
                    name: username,
                    reply: reply_to,
                });
            }
        });
}; // Close onload

function showMessages(msgs) {
    for (let i of msgs) {
        let child = document.createElement("div");
        child.classList.add("message");
        let p = document.createElement('p');
        p.setAttribute("data-id", i.uid);
        p.innerHTML = `<span class='from'>${i.name} - ${i.from}</span>`;
        if (i.hasOwnProperty("reply")) {
            p.innerHTML += `<span class='reply'>${i.reply_text}</span>`;
        }
        p.innerHTML += `<span class='text'>${htmlEnc(i.text)}</span>`;
        let opts = document.createElement("div");
        opts.classList.add("opts");
        opts.innerHTML = `<button class='opt_btn' onclick='reply("${i.uid}")'>Reply</button>`;
        if (id == i.from) {
            child.classList.add("me");
            opts.innerHTML += `
            <button class='opt_btn' onclick='edit(this,"${i.uid}")'>Edt</button>
            <button class='opt_btn' onclick='del_msg("${i.uid}")'>Del</button>
            `;
        }
        p.addEventListener("click", () => {
            document.querySelector(`p[data-id='${i.reply}']`).scrollIntoView();
        });
        child.appendChild(p);
        child.appendChild(opts);
        chats.append(child);
    }
    let froms = msgs.map((msg) => msg.name).join(", ");
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

function edit(elem, uid) {
    let xp = elem.parentElement.parentElement.getElementsByClassName("text")[0];
    xp.setAttribute("contentEditable", true);
    xp.setAttribute("tabindex", "0");
    xp.focus();
    xp.addEventListener("keypress", (e) => {
        if (e.key == "Enter" && !e.shiftKey) {
            e.preventDefault();
            e.target.setAttribute("contentEditable", false);
            e.target.blur();
            socket.emit(
                "edit",
                { uid: uid, text: e.target.innerHTML },
                (e) => {}
            );
        }
    });
    xp.addEventListener("focusout", (e) => {
        e.target.setAttribute("contentEditable", false);
        e.target.setAttribute("tabindex", "None");
        socket.emit("edit", { uid: uid, text: e.target.innerHTML }, (e) => {});
    });
}

function del_msg(uid) {
    socket.emit("delete", { uid: uid });
}

function checkUpdate() {
    socket.emit("update", {}, (data) => {
        if (data.update) {
            eel.log("Updating...");
            eel.update_client(data.url);
        } else {
            eel.log("no update");
        }
    });
}

function reply(uid) {
    let elem = document.querySelector(`p[data-id='${uid}']`);
    let from = elem.getElementsByClassName("from")[0].innerHTML;
    let text = elem.getElementsByClassName("text")[0].innerHTML;
    let str = `<pre>${from}: ${text}</pre>`;
    str = '<span onclick="clearQuote()">x</span>' + str;
    str += `<span class='hidden uid'>${uid}</span>`;
    document.querySelector("#quote").innerHTML = str;
    document.querySelector("#quote").style.display = "block";
    document.querySelector("#msg_input").focus();
    eel.log(elem.innerHTML);
}

function clearQuote() {
    document.querySelector("#quote").innerHTML = "";
    document.querySelector("#quote").style.display = "none";
}
