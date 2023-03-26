import { EXAMPLE_ACTION } from '../actions/types';

const initialState = {
  exampleData: null
};

export default function(state = initialState, action) {
  switch (action.type) {
    case EXAMPLE_ACTION:
      return {
        ...state,
        exampleData: action.payload
      };
    default:
      return state;
  }
}
