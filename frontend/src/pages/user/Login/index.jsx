import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Alert, Button, message, Form } from 'antd';
import { useState } from 'react';
import { ProFormCheckbox, ProFormText, LoginForm } from '@ant-design/pro-form';
import { history, useModel } from 'umi';
import { login } from './service';
import styles from './index.less';
import { setItem } from '@/services/storage/localStorage';

const LoginMessage = ({ content }) => (
  <Alert
    style={{
      marginBottom: 24,
    }}
    message={content}
    type="error"
    showIcon
  />
);

const Login = () => {
  const [userLoginState, setUserLoginState] = useState({});
  const [forgetPass, setForgetPass] = useState(false);
  const [type, setType] = useState('account');
  const { initialState, setInitialState } = useModel('@@initialState');

  const fetchUserInfo = async () => {
    const userInfo = await initialState?.fetchUserInfo?.();

    if (userInfo) {
      await setInitialState((s) => ({ ...s, currentUser: userInfo }));
    }
  };

  const handleSubmit = async (values) => {
    try {
      const resp = await login({ ...values, type });

      if (resp.token) {
        const defaultLoginSuccessMessage = 'Login Success';
        message.success(defaultLoginSuccessMessage);
        setItem('auth_token', resp.token);
        console.log(resp);

        await initialState.setTokenInRequestHeader(resp.token);
        await setInitialState((s) => ({
          ...s,
          request: resp.token,
        }));
        await fetchUserInfo();

        if (!history) return;
        const { query } = history.location;
        const { redirect } = query;
        history.push(redirect || '/');
        return;
      } else throw resp;
    } catch (error) {
      setUserLoginState(error);
      message.error(error.details);
    }
  };
  const tailLayout = {
    wrapperCol: {
      span: 24,
    },
  };
  const { status, type: loginType } = userLoginState;
  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <div className="text-center mt-4">
          <img width={150} alt="logo" src="/logo.png" />
        </div>
        <LoginForm
          initialValues={{
            autoLogin: true,
          }}
          actions={[]}
          onFinish={async (values) => {
            await handleSubmit(values);
          }}
          submitter={{
            render: (props) => (
              <Button
                size="large"
                className="w-100"
                type="primary"
                onClick={() => props.form?.submit()}
              >
                Login
              </Button>
            ),
          }}
        >
          {status === 'error' && loginType === 'account' && (
            <LoginMessage content="Incorrect username/password" />
          )}
          {type === 'account' && (
            <>
              <ProFormText
                name="username"
                fieldProps={{
                  size: 'large',
                  prefix: <UserOutlined className={styles.prefixIcon} />,
                }}
                placeholder="Enter Username"
                rules={[
                  {
                    required: true,
                    message: 'Please input your username!',
                  },
                ]}
              />
              <ProFormText.Password
                name="password"
                fieldProps={{
                  size: 'large',
                  prefix: <LockOutlined className={styles.prefixIcon} />,
                }}
                placeholder="Enter Passworld"
                rules={[
                  {
                    required: true,
                    message: 'Please input your password!',
                  },
                ]}
              />
            </>
          )}

          <div
            style={{
              marginBottom: 24,
            }}
          >
            <ProFormCheckbox noStyle name="autoLogin">
              Remember me
            </ProFormCheckbox>
            <a
              style={{
                float: 'right',
              }}
              onClick={() => {
                setForgetPass(!forgetPass);
              }}
            >
              Forgot Password
            </a>
          </div>
        </LoginForm>
      </div>
      {forgetPass && (
        <Form
          style={{
            margin: 'auto',
            maxWidth: 330,
          }}
          name="basic"
          layout="vertical"
          initialValues={{
            public: '1',
          }}
          onFinish={{}}
        >
          <ProFormText
            name="resetUsername"
            fieldProps={{
              size: 'large',
              prefix: <UserOutlined className={styles.prefixIcon} />,
            }}
            placeholder="Enter Username"
            rules={[
              {
                required: true,
                message: 'Please input your username!',
              },
            ]}
          />
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              block
              onClick={() => {
                history.push('/user/forget-password');
              }}
            >
              Submit
            </Button>
          </Form.Item>
        </Form>
      )}

      {/* <Footer /> */}
    </div>
  );
};

export default Login;
