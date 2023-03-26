import { combineReducers } from 'redux';
import session from './session';
import alert from './alert'
import game from './game';

export default combineReducers({
  session
  ,alert
  ,game
});
