import React, {useEffect, useState} from 'react';
import {Button, Space, Tag, Form, Input, Select} from 'antd';
import { fetchPlayers, createGame } from '../actions/rummyActions';
import { connect, useDispatch } from 'react-redux';

const CreateGame = ({pageData}) => {
    const dispatch = useDispatch();
    useEffect(() => {
      dispatch(fetchPlayers());
    }, []);
    const [playerTags, setPlayerTags] = useState([]);
    const {session, alert} = pageData
    const {allPlayers} = session || {}

    const submit = (values) => {
      let val = {...values}
      Object.keys(val).forEach(key => val[key] === undefined && delete val[key])
      const params = { ...val, players: [...playerTags] }
      dispatch(createGame(params))
    }
    const handleChange = (value) => {
        setPlayerTags(
          [
            ...playerTags
            ,...allPlayers.filter(player => player.id == value)
          ]
        )
    }

    const playerTagsView = () => {
      return playerTags.length > 0 ?
      <Form.Item label=" ">
        <Space size={[0, 8]} wrap>
          { playerTags.map(pTag => <Tag closable onClose={() => closeTag(pTag.id)} key={pTag.id}>{pTag.name}</Tag>) }
        </Space>
        </Form.Item> : ""
    }
    const closeTag = (value) => {
      setPlayerTags(
        [
          ...playerTags.filter(player => player.id != value)
        ]
      )
    }
    const getPlayerOptions = () => {
      console.log(allPlayers, 'from getPlayerOptions')
      return (allPlayers.filter(player => playerTags.indexOf(player) === -1) || []).map(player => getPlayerOption(player))
    }
    const getPlayerOption = (player) => {
      return {value: player['id'], label: player['name'], key: player['id']}
    }
    const getCardInHands = () => {
      const num = playerTags.length
      return num == 1 ? 10 : num <= 3 ? 7 : num <= 5 ? 6 : 0
    }
    return (
        <Form
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            style={{ maxWidth: 600 }}
            initialValues={{ remember: true }}
            // onFinish={onFinish}
            // onFinishFailed={onFinishFailed}
            autoComplete="off"
            onFinish={submit}
        >
            <Form.Item
              label="Select Players"
              name="players"
              rules={[
                  { required: true, message: 'Please select number of players!' }
              ]}
              >
              <Select
                  onChange={handleChange}
                  options={getPlayerOptions()}
                  disabled = { playerTags.length >= 6 ? true : false}
              />
            </Form.Item >
            { playerTagsView() }
            
            <Form.Item
              label="Number of cards in a hand"
              // name="num_of_cards_in_hand"
              // value = {getCardInHands()}
              
              >
              {getCardInHands()}
            </Form.Item >

            <Form.Item
              label="Finish Mark"
              name="finish_mark"
              initialValue = "100"
              >
              <Input />
            </Form.Item  >
            

            

            {/* <Form.Item name="remember" valuePropName="checked" wrapperCol={{ offset: 8, span: 16 }}>
            <Checkbox>Remember me</Checkbox>
            </Form.Item> */}

            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit" >
                Submit
            </Button>
            </Form.Item>
        </Form>
    )
};

// export default LoginForm;
const mapStateToProps = state => ({
    pageData: {...state}
  });
  
  export default connect(mapStateToProps, { fetchPlayers })(CreateGame);