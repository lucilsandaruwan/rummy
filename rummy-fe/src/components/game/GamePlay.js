import React, { useEffect, useState } from 'react';
import {Row, Col, Card, Collapse, Space, Tag, Popover, Spin, notification, Modal} from 'antd';
import { loadGame } from '../../actions/rummyActions';
import { connect, useDispatch } from 'react-redux';
import styles from './Game.module.css'
import RoundHands from './RoundHands'
import StockFiles from './StockPiles'

const { Panel } = Collapse;
const GamePlay = ({gameData}) => {
    const [api, contextHolder] = notification.useNotification();
    const {game} = gameData 
    const { hands, is_started } = game || {}
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(loadGame());
        openNotification('right')
    }, []);
    
    const openNotification = (placement) => {
        api.info({
        message: `Notification ${placement}`,
        description:
            'This is the content of the notification. This is the content of the notification. This is the content of the notification.',
       
        });
    };
    
    
    

    const getHands = () => {
        const handcp = hands || []
        const index = handcp.findIndex(hand => hand.id !== undefined);
        const spanNum = parseInt(24/handcp.length)
        const preHands = handcp.slice(0, index);
        const postHands = handcp.slice(index + 1);
        const currentHand = handcp[index];
        const allHands = [currentHand, ...postHands, ...preHands]
        return allHands.map((hand, idx) => {
            if(hand) {
                return <RoundHands hand={hand} spanNum={spanNum} key={idx}/>
            }
            
        })
    }

    return (
        <div>
            {contextHolder}
            
            <Row gutter={16} span={24}>
              <Col span={18}> 
                <Row gutter={16}>
                    {getHands()}
                </Row>
              </Col> 
              {/* end usesrs */}
              <Col span={6}>
                <StockFiles/>
              </Col>}
              
            </Row>
        </div>
    )
};

const mapStateToProps = state => ({
    gameData: {...state}
  });
  
  export default connect(mapStateToProps, { loadGame })(GamePlay);