export default [
  {
    path: '/user',
    layout: false,
    routes: [
      {
        path: '/user',
        routes: [
          {
            name: 'login',
            path: '/user/login',
            component: './user/Login',
          },

          {
            path: '/user/tracking',
            component: './TrackParcel',
            name: 'Parcel Tracking',
            icon: 'FolderOpenOutlined',
          },
        ],
      },
      {
        component: './404',
      },
    ],
  },
  {
    path: '/welcome',
    name: 'welcome',
    icon: 'smile',
    component: './Welcome',
  },
  {
    path: '/admin',
    name: 'admin',
    icon: 'crown',
    access: 'canAdmin',
    component: './Admin',
    routes: [
      {
        path: '/admin/sub-page',
        name: 'sub-page',
        icon: 'smile',
        component: './Welcome',
      },
      {
        component: './404',
      },
    ],
  },
  {
    access: 'canAdmin',
    name: 'User Management',
    icon: 'user',
    path: '/users',
    component: './UserManagement',
  },
  {
    name: 'Branch Management',
    icon: 'BankOutlined',
    access: 'canAdmin',
    path: '/branch',
    routes: [
      {
        path: '/branch/branches',
        component: './BranchManagement',
        name: 'Branch Management',
        icon: 'BankOutlined',
      },
      {
        path: '/branch/routing',
        component: './Routing',
        name: 'Routing',
        icon: 'LinkOutlined',
      },
    ],
  },
  {
    path: '/parcel',
    icon: 'table',
    name: 'Parcel Management',
    routes: [
      {
        path: '/parcel/parcel-management',
        component: './ParcelManagement',
        name: 'Parcel Management',
        icon: 'FolderOpenOutlined',
      },
      {
        path: '/parcel/receive',
        component: './ReceiveParcel',
        name: 'Parcel Receive',
        icon: 'FolderOpenOutlined',
        access: 'canOfficeStaff',
      },
      {
        path: '/parcel/route',
        component: './RouteParcel',
        name: 'Parcel Route',
        icon: 'FolderOpenOutlined',
        access: 'canOfficeStaff',
      },
    ],
  },
  {
    path: '/',
    redirect: '/welcome',
  },
  {
    component: './404',
  },
];
