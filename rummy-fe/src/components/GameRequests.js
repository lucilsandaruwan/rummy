import React, {useEffect, useState} from 'react';
import {Space, Table, Tag, Button} from 'antd';
import { fetchHands, acceptHand, declineHand } from '../actions/rummyActions';
import { connect, useDispatch } from 'react-redux';

const GameRequests = ({pageData}) => {
    const dispatch = useDispatch();
    const {session} = pageData || {}
    const { hands } = session || {}
    useEffect(() => {
      dispatch(fetchHands());
    }, []);

    const acceptHandler = (id) => {
      dispatch(acceptHand(id))
    } 

    const declineHandler = (id) => {
      dispatch(declineHand(id))
    } 
    const getTableData = () => {
      return (hands || []).map(element => {
        const {hand, creator} = (element || {})
        const {name} = (creator || {})
        const {hand_id} = (hand || {})
        return {
          key: hand_id,
          name: name,
          id: hand_id
        }
      });
    }
    const columns = [
      {
        title: 'Creator Name',
        dataIndex: 'name',
        key: 'name',
      },
      {
        title: 'Action',
        key: 'action',
        render: (_, record) => (
          <Space size="middle">
            <Button onClick = {() => acceptHandler(record.id)} > Accept</Button>
            <Button onClick = {() => declineHandler(record.id)} > Decline</Button>
          </Space>
        ),
      },
    ];
    
    return (
      <Table columns={columns} dataSource={getTableData()}/>
    )
};

// export default LoginForm;
const mapStateToProps = state => ({
    pageData: {...state}
  });
  
  export default connect(mapStateToProps, {fetchHands, acceptHand, declineHand})(GameRequests);