import { Server } from "socket.io";

const io = new Server(3000);

const sleep = (ms = 1000) => new Promise((resolve) => setTimeout(resolve, ms));

const connections = {};

let serverDate = new Date();
console.log(`Initial server date: ${serverDate.toISOString()}`);
let responseCount = 0;

io.on("connection", async (socket) => {
  console.log(`Novo cliente conectado: ${socket.id}`);

  connections[socket.id] = {
    ...connections[socket.id],
    socket: socket,
    diffInSeconds: 0,
  };

  socket.on("sync:diff", (data) => {
    responseCount++;
    const diffTimeClient = data.diff;

    connections[socket.id] = {
      ...connections[socket.id],
      diffInSeconds: diffTimeClient,
    };

    if (responseCount >= 4) {
      const sumTimeInSeconds = Object.values(connections).reduce(
        (acc, curr) => {
          return acc + curr.diffInSeconds;
        },
        0
      );

      const meanTime = sumTimeInSeconds / Object.keys(connections).length;

      serverDate.setSeconds(serverDate.getSeconds() + meanTime);

      for (let key of Object.keys(connections)) {
        const diffTime = connections[key].diffInSeconds;
        if (diffTime < 0) {
          connections[key].socket.emit(
            "sync:time:client",
            Math.abs(diffTime + meanTime)
          );
        } else {
          connections[key].socket.emit(
            "sync:time:client",
            diffTime * -1 + meanTime
          );
        }
      }

      console.log(`Server date: ${serverDate.toISOString()}`);

      responseCount = 0;
    }
  });

  if (Object.keys(connections).length >= 4) {
    const date = new Date();

    io.emit("sync:time", date.toISOString());
  }
});

io.on("disconnect", (socket) => {
  delete connections[socket.id];
});
