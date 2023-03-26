import axios from 'axios';
import { LOGIN, ALERT, FETCH_PLAYERS, SET_HANDS, UPDATE_GAME } from './types';
axios.defaults.baseURL = 'http://localhost:8080/';
axios.defaults.headers.post['Content-Type'] ='application/json;charset=utf-8';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

export const fetchSession = () => dispatch => {
  axios.get('/fetch_user', { 
    withCredentials: true 
  })
    .then(res => {
      const {data} = res
      const {isLogin, roomId, name, hands} = data
      dispatch({
        type: LOGIN,
        payload: {
            isLogin,
            name,
            roomId,
            hands
        }
      })
    })
    .catch(err => console.log(err, "error"));
};

export const login = (values, postLogin) => async dispatch => {
  console.log({...values})
  axios.post("login"
  ,{
    ...values
  },{
    withCredentials: true
  }).then(res => {
      const {data} = res
      const {status, message} = data || {}
      const {isLogin, room_id, name, hands} = message
      if (status == "success") {
        dispatch({
          type: LOGIN,
          payload: {isLogin, room_id, name, hands}
        });
      } else {
        dispatch(alertm(status, message))
      }
      
  })
  .catch(
    err => console.log(err, "error")
  );
}

export const logout = (postLogout) => dispatch => {
  axios.get("logout/"
  ,{
    withCredentials: true
  }).then(res => {
      dispatch({
        type: LOGIN,
        payload: {
            player: {email: "", chnl: ""}
            ,game: {}
        }
      });
      dispatch(postLogout)
  })
  .catch(err => console.log(err, "error"));
}

export const alertm = (status, message) => dispatch => {
  dispatch({
    type: ALERT,
    payload: {
        status
        ,message
    }
  });
  setTimeout(() => {
    dispatch({
      type: ALERT,
      payload: {
          status: false
      }
    });
  }, 2000);
}

export const loadGame = () => dispatch => {
  axios.get('load_game', { 
    withCredentials: true 
  }).then(reslt => {
    const {data: res} = reslt || {}
    const {data} = res || {}
    const {hands} = data || {hands: []}


    dispatch({
      type: UPDATE_GAME,
      payload: {...data, 'all_accepted': hands.every(h => h.is_accepted == 'accepted')}
    });
  }).catch(err => console.log(err, "error"));
}


export const createGame = (params) => dispatch => {
  axios.post('create_game', {... params} ,{withCredentials: true}).then(res => {
    const {data} = res
      const {status, message} = data || {}
      const {isLogin, room_id, name} = message
      if (status == "success") {
        console.log("success")
        // dispatch({
        //   type: CREATE_GAME,
        //   payload: {isLogin, room_id, name}
        // });
      } else {
        dispatch(alertm(status, message))
      }
  }).catch(err => console.log(err))
}

export const fetchPlayers = () => dispatch => {
  axios.get('fetch_players', { 
    withCredentials: true 
  }).then(rest => {
    const {data} = rest || {}
    dispatch({
      type: FETCH_PLAYERS,
      payload: data
    });
  }).catch(err => console.log(err, "error"));
}

export const fetchHands = () => dispatch => {
  axios.get('fetch_hands', { 
    withCredentials: true 
  }).then(rest => {
    const {data} = rest || {}
    dispatch({
      type: SET_HANDS,
      payload: data
    });
  }).catch(err => console.log(err, "error"));
}

export const acceptHand = (id) => dispatch => {
  axios.post('accept_hand', {id} ,{withCredentials: true}).then(res => {
    const {data, status, message} = res || {}
      if (status == "success") {
        dispatch({
          type: SET_HANDS,
          payload: [...data]
        });
        dispatch(alertm(status, "Game request accepted!"))
      } else {
        dispatch(alertm(status, message))
      }
  }).catch(err => console.log(err))
}

export const declineHand = (id) => dispatch => {
  axios.post('decline_hand', {id} ,{withCredentials: true}).then(res => {
    const {data: data1} = (res || {})
    const {data, status, message} = (data1 || {})
      if (status == "success") {
        console.log("success decline", data)
        dispatch({
          type: SET_HANDS,
          payload: [...data]
        });
        dispatch(alertm(status, "Game request declinec!"))
      } else {
        dispatch(alertm(status, message))
      }
  }).catch(err => console.log(err))
}

export const startGame = () => dispatch => {
  axios.post('start_game', {withCredentials: true}).then(res => {
    
  }).catch(err => console.log(err))
}