import { ALERT } from '../actions/types';
import { Alert } from 'antd';

const initialState = {
  alert: {}
};

export default function(state = initialState, action) {
  switch (action.type) {
    case ALERT:
      return {
        ...state
        ,...action.payload
      };
    default:
      return state;
  }
}
