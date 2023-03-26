import React, { useEffect, useState } from 'react';
import {Breadcrumb, Layout, Menu, theme, Alert } from 'antd';
import { UserOutlined, AimOutlined} from '@ant-design/icons';
import { connect, useDispatch } from 'react-redux';
import LoginForm from './LoginForm';
import Game from './game/Game'
import CreateGame from './CreateGame'
import Home from './Home'
import { fetchSession, logout} from '../actions/rummyActions';
import {connectToServer, joinUserRoom} from "../actions/realTimeActions"
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import GameRequests from './GameRequests'

const { Header, Content, Footer, Sider } = Layout;

function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}




const RummyComponent = ({ pageData }) => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const lPath = location.pathname
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const dispatch = useDispatch();
  useEffect(() => {
    console.log("changed")
    dispatch(fetchSession());
  }, []);

  
  const {session, alert} = pageData
  const {isLogin = 0, roomId, hands} = session || {hands: []}
  const navigate = useNavigate();

  useEffect(() => {
    console.log(roomId, isLogin, 'test useEffect')
    if (roomId) {
      dispatch(joinUserRoom(roomId));
    }
  }, [roomId]);

  // useEffect(() => {
  //   console.log(pageData, 'pageDataxxx')
  //   console.log('changed isLogin', isLogin)
  //   if (!isLogin) {
  //     navigate('/login')
  //   } else {
  //     navigate('/')
  //   }
  // }, [isLogin]);

  console.log(pageData, 'page data')
  const {status, message} = alert || {}
  const userAction = isLogin ? 'logout': 'login'

  let items =   [getItem('User', 'sub1', <UserOutlined />,[getItem(userAction, userAction)])];
  const getSubItems = () => {
    const firstHand = (hands || []).length > 0 ? hands[0] : {}
    const {hand} = (firstHand || {})
    const {is_accepted} = (hand || {})
    return is_accepted == 'accepted' ? [(getItem('Play', 'game'))] 
        : is_accepted ? [(getItem('Game Requests', 'requests'))] : [getItem('Create Game', 'create_game')]
  }
  let gameItems = isLogin ? [getItem( 'Game','sub2', <AimOutlined/>, getSubItems())] : []

  let mitems = [...items, ...gameItems]

  const postLogout = () => {
    navigate('/login')
  }
  
  const menueClick = (item ) => {
      if (item['key'] == 'logout') {
        dispatch(logout(postLogout))
      } else if (item['key'] == 'create_game') {
        navigate('/create-game')
      } else if (item['key'] == 'requests') {
        navigate('/requests')
      } else if (item['key'] == 'game') {
        navigate('/game')
      }
  }
  const breadcrumbMapping = (path) => {
    const mapping = {
      '/login': 'Login'
      ,'/create-game': "Create Game"
      ,'/requests': 'Game Requests'
      ,'/game': 'Game'
    }
    return mapping[path] || 'Home'
  }
  
  return (
    <Layout
      style={{
        minHeight: '100vh',
      }}
    >
      <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
        <div
          style={{
            height: 32,
            margin: 16,
            background: 'rgba(255, 255, 255, 0.2)',
          }}
        />
        <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={mitems} onClick = {menueClick} />
      </Sider>
      <Layout className="site-layout">
        {status && <Alert message = {message} type={status} /> }
        <Header
          style={{
            padding: 0,
            background: colorBgContainer,
          }}
        />
        <Content
          style={{
            margin: '0 16px',
          }}
        >
          <Breadcrumb
            style={{
              margin: '16px 0',
            }}
          >
            <Breadcrumb.Item>Rummy Game</Breadcrumb.Item> 
          <Breadcrumb.Item>{ breadcrumbMapping(lPath)}</Breadcrumb.Item>
          </Breadcrumb>
          <div
            style={{
              padding: 24,
              minHeight: 360,
              background: colorBgContainer,
            }}
          >
            { 
                !isLogin ? <LoginForm/> :
                <Routes>
                  <Route path="/" element={<Home/>} />
                  <Route path="/login" element={<LoginForm/>} />
                  <Route path="/create-game" element={<CreateGame/>} />
                  <Route path="/requests" element={<GameRequests/>} />
                  <Route path="/game" element={<Game/>} />
                  
                </Routes>
            }
          </div>
        </Content>
        <Footer
          style={{
            textAlign: 'center',
          }}
        >
          
        </Footer>
      </Layout>
    </Layout>
    
  );
};

const mapStateToProps = state => ({
  pageData: {...state}
});

export default connect(mapStateToProps, { fetchSession, logout, connectToServer})(RummyComponent);







