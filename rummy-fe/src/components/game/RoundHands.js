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
            <Card  className={styles.card} title={hand.name} bordered={false}
                actions={id ?[
                    <button onClick={showModal}>New set</button>,
                    <button onClick={showModal}>New run</button>,
                ]: []}
            >
                <Collapse size={"small"}>
                    <Panel header="Hand" key={key}>
                        <Collapse accordion={true} size={"small"} collapsible={!id ? "disabled" : ""} >
                            <Panel className={styles.hand} showArrow={false} header="&clubs; A" key="1" >
                                {id ? <><button>Discard</button> <button>Lay off</button></>: ''}
                            </Panel>  
                            <Panel className={styles.hand} showArrow={false} header="&spades; 8" key="2">
                                <p>{text}</p>
                            </Panel>
                            <Panel showArrow={false} header= {<div className={[styles.hand,styles.red].join(' ')} >&diams; 10</div> } key="3">
                                <p>{text}</p>
                            </Panel>  
                        </Collapse>
                    </Panel>
                    <Panel header="Runs" key="2">
                        <Collapse defaultActiveKey="1">
                            <Panel header="&clubs; A" key="1">
                                <p>{text}</p>
                            </Panel>  
                            <Panel header="&spades; 8" key="2">
                                <p>{text}</p>
                            </Panel>
                            <Panel className={styles.red} header= {<div className={styles.red}>&diams; 10</div> } key="3">
                                <p>{text}</p>
                            </Panel>  
                        </Collapse>
                    </Panel>
                    <Panel className={styles.red} header="Sets" key="3">
                        <Collapse defaultActiveKey="1">
                            <Panel header="&clubs; A" key="1">
                                <p>{text}</p>
                            </Panel>  
                            <Panel header="&spades; 8" key="2">
                                <p>{text}</p>
                            </Panel>
                            <Panel className={styles.red} header= {<div className={styles.red}>&diams; 10</div> } key="3">
                                <p>{text}</p>
                            </Panel>  
                        </Collapse>
                    </Panel>
                </Collapse>
            </Card>
            <Modal title="Basic Modal" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
                <p>Some contents...</p>
                <p>Some contents...</p>
                <p>Some contents...</p>
            </Modal>
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