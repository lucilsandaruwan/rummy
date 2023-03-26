import React, { useEffect, useState } from 'react';
import {Row, Col, Card, Collapse, Space, Tag, Popover, Spin, notification, Modal} from 'antd';
import styles from './Game.module.css'
const { Panel } = Collapse;
const Hand = (props) => {
    console.log(props, 'props')
    const {hand, spanNum, key} = props || {}
    const {is_accepted, name, id} = hand || {}
    const [isModalOpen, setIsModalOpen] = useState(false);

    
    

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const text = `
        A dog is a type of domesticated animal.
        Known for its loyalty and faithfulness,
        it can be found as a welcome guest in many households across the world.
        `;
    const getCard = () => (
        <Col>
            <Card  className={styles.card} title={hand.name} bordered={false}>
                <span>{is_accepted == 'accepted' ? 'Accepted': "Pending"}</span>
            </Card>
            
        </Col>
    );
    const notAccepted = (element) => {
        return (<Spin tip="Waiting to Accept" size="large">
            {element}
        </Spin>)
    }

    console.log(is_accepted, '')
    return (
        <Col span={spanNum}>
            {is_accepted == 'pending' ? notAccepted(getCard()) : getCard()}
        </Col>
    ) 
}

export default Hand;