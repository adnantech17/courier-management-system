import { PageContainer } from '@ant-design/pro-layout';
import { Card, Alert, Typography } from 'antd';
import styles from './Welcome.less';
import { useModel } from 'umi';

const CodePreview = ({ children }) => (
  <pre className={styles.pre}>
    <code>
      <Typography.Text copyable>{children}</Typography.Text>
    </code>
  </pre>
);

const Welcome = () => {
  const { initialState } = useModel('@@initialState');
  const { currentUser } = initialState || {};
  return (
    <PageContainer>
      <Card>Welcome, {currentUser?.name}</Card>
    </PageContainer>
  );
};

export default Welcome;
