const net = require("net");

const socket = new net.Socket();

socket.connect(5000, "localhost", () => {
  console.log("Conectado ao servidor!");

  socket.write("ping");
});

socket.on("data", (data) => {
  const message = data.toString().trim();

  console.log(`Mensagem recebida do servidor: "${message}"`);

  if (message === "pong") {
    socket.write("alo");
  } else if (message === "ok") {
    socket.write("");
  }
});

socket.on("end", () => {
  console.log("Conexão encerrada!");
});
