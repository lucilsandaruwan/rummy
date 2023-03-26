import { UPDATE_GAME } from '../actions/types'
const initialState = {
    
  };

export default function(state = initialState, action) {
    switch (action.type) {
        case UPDATE_GAME:
            return {
                ...state
                ,...action.payload
            };
        default:
            return state;
    }
}