import { ConfigProvider, message } from 'antd';
import { PageLoading } from '@ant-design/pro-layout';
import 'antd/dist/antd.css';
import enUS from 'antd/lib/locale/en_US';
import { history } from 'umi';
import RightContent from '@/components/RightContent';
import { getCurrentUser as queryCurrentUser } from './pages/user/Login/service';
import { request } from '@/services/api/client';
// import { onMessage } from "firebase/messaging";
// import { messaging } from "@/services/firebase/firebaseInit";
const loginPath = '/user/login';

const publicPaths = ['/user/login', '/user/forget-password'];

export const initialStateConfig = {
  loading: <PageLoading />,
};
/**
 * @see  https://umijs.org/zh-CN/plugins/plugin-initial-state
 * */

export async function getInitialState() {
  const token = localStorage.getItem('auth_token');
  let currentUser;

  const setTokenInRequestHeader = async (token) => {
    request.interceptors.request.use((url, options) => {
      if (token) {
        options.headers['Authorization'] = `Token ${token}`;
      } else {
        delete options.headers['Authorization'];
      }

      return {
        url: `${url}`,
        options: { ...options, interceptors: true },
      };
    });
  };

  const fetchUserInfo = async () => {
    try {
      const msg = await queryCurrentUser();
      if (msg.success) return msg.data;
      else throw Error();
    } catch (error) {
      localStorage.removeItem('auth_token');
      setTokenInRequestHeader(null);
      history.push(loginPath);
    }
  };

  if (token) {
    setTokenInRequestHeader(token);
    currentUser = await fetchUserInfo();
  }

  return {
    fetchUserInfo,
    setTokenInRequestHeader,
    settings: {},
    currentUser,
  };
}

export const layout = ({ initialState, setInitialState }) => {
  return {
    logo: null,
    rightContentRender: () => <RightContent />,
    disableContentMargin: false,
    onPageChange: () => {
      const { location } = history;

      if (!initialState?.currentUser && location.pathname !== loginPath) {
        history.push(loginPath);
      }
    },
    childrenRender: (children, props) => {
      return <ConfigProvider locale={enUS}>{children}</ConfigProvider>;
    },
    ...initialState?.settings,
  };
};
