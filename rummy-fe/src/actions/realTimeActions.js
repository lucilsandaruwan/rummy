import io from 'socket.io-client'
import {GAME_REQS} from './types'
const socket = io('http://localhost:8080');


// export const testRT = () => dispatch => {
//   axios.get("rt-test/"
//   ,{
//     withCredentials: true
//   }).then(res => {
//     connectToServer(dispatch);
//   })
//   .catch(err => console.log(err, "error"));
// }

export const connectToServer = (dispatch) => {
  alert("test connect")
  socket.on('connect', (data) => {
    console.log('connected to server', data);
    dispatch({ type: 'SOCKET_CONNECTED', payload: socket });
  });
  
  socket.emit('join', {'room': 'test_room'});
  socket.on("message", function (msg) {
    console.log("Received sensorData message :: " + msg);
  });
};

export const joinUserRoom = (room_id) => dispatch => {
  socket.on('connect', (data) => {
    console.log('connected to server', data);
    // dispatch({ type: 'SOCKET_CONNECTED', payload: socket });
  });
  socket.emit('join', {'room': room_id});
  socket.on("game_invitation", function (msg) {
    dispatch({type: GAME_REQS, payload: msg})
  });
}
