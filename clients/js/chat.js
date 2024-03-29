/*
 * Copyright 2020 The NATS Authors
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { connect, JSONCodec, credsAuthenticator } from "/node_modules/nats.ws/esm/nats.js";

const creds = ``;

window.chat = {
  send: send,
  exiting: exiting,
  modalExit: modalExit,
  modalInit: modalInit,
};

// create a decoder, the client is sending JSON
const jc = JSONCodec();

// create a connection, and register listeners
const init = async function () {
  // if the connection doesn't resolve, an exception is thrown
  // a real app would allow configuring the hostport and whether
  // to use WSS or not.
  modalInit()
  addDestination()
  const me = window.localStorage.getItem("user");
  const conn = await connect(
    { servers: window.localStorage.getItem("server"),
      authenticator: credsAuthenticator(new TextEncoder().encode(creds)),
     },
  );

  // handle connection to the server is closed - should disable the ui
  conn.closed().then((err) => {
    let m = "NATS connection closed";
    addEntry(`${m} ${err ? err.message : ""}`);
  });
  (async () => {
    for await (const s of conn.status()) {
      addEntry(`Received status update: ${s.type}`, '#337ab795');
    }
  })().then();

  // the chat application listens for messages sent under the subject 'chat'
  (async () => {
    const chat = conn.subscribe(`${me}.ping`);
    for await (const m of chat) {
      protobuf.load("message/pingpong.proto")
      .then(function(root) {
         const messageType = root.lookupType("pingpong.PingRequest");
         const message = messageType.decode(m.data);
         if (message.origin != me) {
            addEntry(
              `(${message.origin}): ${message.message}`, '#F5F5F5',
            );
          }
      });

    }
  })().then();

  // when a new browser joins, the joining browser publishes an 'enter' message
  (async () => {
    const enter = conn.subscribe(`${me}.enter`);
    for await (const m of enter) {
      const jm = jc.decode(m.data);
      addEntry(`${jm.id} entered.`, '#337ab795');
    }
  })().then();

  (async () => {
    const exit = conn.subscribe(`${me}.exit`);
    for await (const m of exit) {
      const jm = jc.decode(m.data);
      if (jm.id !== me) {
        addEntry(`${jm.id} exited.`, '#337ab795');
      }
    }
  })().then();

  // we connected, and we publish our enter message
  conn.publish(`${me}.enter`, jc.encode({ id: me }));
  return conn;
};

init().then((conn) => {
  window.nc = conn;
}).catch((ex) => {
  addEntry(`Error connecting to NATS: ${ex}`, '#337ab795');
});

// this is the input field
let input = document.getElementById("data");
// add a listener to detect edits. If they hit Enter, we publish it
input.addEventListener("keyup", (e) => {
  if (e.key === "Enter") {
    document.getElementById("send").click();
  } else {
    e.preventDefault();
  }
});

// send a message if user typed one
function send() {
  const me = window.localStorage.getItem("user");
  const destination = window.localStorage.getItem("destination");
  input = document.getElementById("data");
  const m = input.value;
  if (m !== "" && window.nc) {
    protobuf.load("message/pingpong.proto")
    .then(function(root) {
      const messageType = root.lookupType("pingpong.PingRequest");
      var payload = {
        destination: destination,
        origin: me,
        message:m
      };
      var message = messageType.create(payload);
      addEntry(
        message.origin === me ? `(me): ${message.message}` : `(${message.origin}): ${message.message}`, '#337ab750',
      );
      var buffer = messageType.encode(message).finish();
      window.nc.publish(`${me}.ping`, buffer);
      input.value = "";
    });
  }
  return false;
}

// send the exit message
function exiting() {
  if (window.nc) {
    window.nc.publish(`${me}.exit`, jc.encode({ id: me }));
  }
}

// add an entry to the document
function addEntry(s, color) {
  const p = document.createElement("pre");
  p.appendChild(document.createTextNode(s));
  p.style.backgroundColor = color
  document.getElementById("chats").appendChild(p);
}

function addDestination() {
  const me = window.localStorage.getItem("user");
  const destination = window.localStorage.getItem("destination");
  document.getElementById("destination").innerHTML = `from ${me ? me : "null"} to ${destination ? destination : "null"}`;
}

function modalInit(){
  const me = window.localStorage.getItem("user");
  const destination = window.localStorage.getItem("destination");
  const server = window.localStorage.getItem("server");
  if (me != null){
    document.getElementById("user").value = me
  }
  if (destination != null){
    document.getElementById("user-destination").value = destination
  }
  if (server != null){
    document.getElementById("server").value = server
  }
}

function modalExit(){
  window.localStorage.user = document.getElementById("user").value;
  window.localStorage.destination = document.getElementById("user-destination").value;
  window.localStorage.server = document.getElementById("server").value;

  init()
  return false;
}
