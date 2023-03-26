import React, { useEffect, useState } from 'react';
import {Row, Col, Card, Collapse, Space, Tag, Button, Spin, notification, Modal} from 'antd';
import { startGame } from '../../actions/rummyActions';
import { connect, useDispatch } from 'react-redux';
import styles from './Game.module.css'
import Hand from './Hand'
import StockFiles from './StockPiles'

const { Panel } = Collapse;
const GameWaiting = ({gameData}) => {
    const [api, contextHolder] = notification.useNotification();
    const {game} = gameData 
    const { hands, all_accepted } = game || {}
    const dispatch = useDispatch();
    useEffect(() => {
        openNotification('right')
    }, []);
    
    const openNotification = (placement) => {
        api.info({
        message: `Notification ${placement}`,
        description:
            'This is the content of the notification. This is the content of the notification. This is the content of the notification.',
       
        });
    };
    const startGame = () => {
        dispatch(startGame())
    }
    
    
    

    const getHands = () => {
        const handcp = hands || []
        const index = handcp.findIndex(hand => hand.id !== undefined);
        const spanNum = parseInt(24/handcp.length)
        const preHands = handcp.slice(0, index);
        const postHands = handcp.slice(index + 1);
        const currentHand = handcp[index];
        const allHands = [currentHand, ...postHands, ...preHands]
        return allHands.map((hand, idx) => {
            console.log(hand,idx, 'haaaaa')
            if(hand) {
                return <Hand hand={hand} spanNum={spanNum} key={idx}/>
            }
            
        })
    }

    return (
        <div>
            {contextHolder}
            {all_accepted ? <Row>
                <Col >
                <Button onClick={startGame} className={styles.start_button} type="dashed" danger>
                    Start
                </Button>
                </Col>
            </Row> : ""}
            <Row gutter={16} span={24}>
                {getHands()}
            </Row>
        </div>
    )
};

const mapStateToProps = state => ({
    gameData: {...state}
  });
  
  export default connect(mapStateToProps, { startGame })(GameWaiting);