import { LOGIN, FETCH_PLAYERS, SET_HANDS } from '../actions/types';

const initialState = {
  isLogin: false
  ,game:{}
  ,allPlayers: []
  ,hands: []
};

export default function(state = initialState, action) {
  switch (action.type) {
    case LOGIN:
      return {
        ...state
        ,isLogin: action.payload.isLogin
        ,roomId: action.payload.roomId
        ,name: action.payload.name
        ,game: action.payload.game
        ,hands: action.payload.hands
      };
    case FETCH_PLAYERS:
      return {
          ...state
          ,allPlayers: [...action.payload || []]
      };
    case  SET_HANDS:
      return {
          ...state  
          ,hands: [...action.payload]
      };
    default:
      return state;
  }
}



