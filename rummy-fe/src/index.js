import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import store from './store/store';
import RummyComponent from './components/RummyComponent';
import { BrowserRouter } from 'react-router-dom';
import './styles/main.scss';

ReactDOM.render(
  <Provider store={store}>
    
    <BrowserRouter>
      <RummyComponent />
    </BrowserRouter>
    
  </Provider>,
  document.getElementById('root')
);
