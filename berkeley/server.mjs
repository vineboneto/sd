import { Server } from 'socket.io'

const io = new Server(3000)

const sleep = (ms = 1000) => new Promise((resolve) => setTimeout(resolve, ms))

let responses = []
const connections = new Map()
const TIME_SYNC_INTERVAL_MS = 1000 * 10 // sync time every 5 seconds

io.on('connection', (socket) => {
  console.log(`Novo cliente conectado: ${socket.id}`)

  connections.set(socket.id, { ...connections.get(socket.id), socket })

  const p = new Promise((resolve) => {
    socket.on('sync:diff', (data) => {
      // store the data
      connections.set(socket.id, { ...connections.get(socket.id), diffInSeconds: data.diff })

      resolve()
    })
  })

  responses.push(p)

  setInterval(() => {
    if (connections.size === 0) return

    // send the time to all clients
    const date = new Date()
    console.log(`Initial server date: ${date.toISOString()}`)
    io.emit('sync:time', date.toISOString())

    Promise.all(responses)
      .then(() => {
        // calcular media
        const sumTimeInSeconds = Array.from(connections.values()).reduce((acc, curr) => acc + curr.diffInSeconds, 0)
        const meanTime = sumTimeInSeconds / connections.size

        // ajustar tempo servidor
        date.setSeconds(date.getSeconds() + meanTime)

        // notificar clientes
        for (let key of connections.keys()) {
          const diffTime = connections.get(key).diffInSeconds

          if (diffTime < 0) connections.get(key).socket.emit('sync:time:client', Math.abs(diffTime + meanTime))
          else connections.get(key).socket.emit('sync:time:client', diffTime * -1 + meanTime)
        }

        console.log(`Server date: ${date.toISOString()}`)
      })
      .catch(console.error)
      .finally(() => {
        responses = []
      })
  }, TIME_SYNC_INTERVAL_MS)
})
