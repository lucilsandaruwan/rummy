import React, { useEffect } from 'react';
import GameWaiting from './GameWaiting'
import GamePlay from './GamePlay'
import { loadGame } from '../../actions/rummyActions';
import { connect, useDispatch } from 'react-redux';

const Game = ({gameData}) => {
    const {game} = gameData 
    const { is_started } = game || {}
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(loadGame());
    }, []);
    
    return is_started == 1 ? <GamePlay/> : <GameWaiting/>
};

const mapStateToProps = state => ({
    gameData: {...state}
});
  
  export default connect(mapStateToProps, { loadGame })(Game);