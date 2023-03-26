import React, { useEffect } from 'react';
import {Button, Checkbox, Form, Input} from 'antd';
import { login } from '../actions/rummyActions';
import { connect, useDispatch } from 'react-redux';
import {useNavigate} from 'react-router-dom';

const LoginForm = (data) => {
    const {pageData} = data || {}
    const {session} = pageData;
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const submit = (values) => {
        dispatch(login(values, postLogin))
    }
    const { hands, isLogin } = session || {}
    useEffect(() => {
        console.log("changed")
        postLogin()
    }, [hands]);
    const postLogin = () => {
        const firstHand = (hands || []).length > 0 ? hands[0] : {}
        const {hand} = (firstHand || {})
        const {is_accepted} = (hand || {})
        if (is_accepted == 'accepted'){
            navigate('/game')
        } else if(is_accepted) {
            navigate('/requests')
        } else if(isLogin) {
            navigate('/')
        }
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
            label="Email"
            name="email"
            rules={[
                { required: true, message: 'Please input your email!' }
                , {pattern: /^[A-Za-z0-9._+\-\']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/, message: 'Please input the email in corret format!'}
            ]}
            >
            <Input />
            </Form.Item>

            <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
            >
            <Input.Password />
            </Form.Item>

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
  
  export default connect(mapStateToProps, { login })(LoginForm);