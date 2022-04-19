import React, { useEffect, useState } from 'react';
import ProForm, { ProFormDigit, ProFormMoney, ProFormSelect } from '@ant-design/pro-form';
import { Col, message, Modal, Row } from 'antd';
import { branchLinkCreate, getBranchesForDropdown } from '../service';

const Form = (props) => {
  const { modalVisible, onSuccess, onCancel, name, title, values } = props;
  const [form] = ProForm.useForm();

  useEffect(() => form.setFieldsValue(values), [values]);

  const handleSubmit = async () => {
    try {
      const validatedData = await form.validateFields();
      const resp = await branchLinkCreate({ ...validatedData, id: values?.id });
      const resp2 = await branchLinkCreate({
        ...validatedData,
        id: values?.id,
        from_branch: validatedData.from_branch,
        to_branch: validatedData.to_branch,
      });
      if (!resp.success || !resp2.success) throw resp;
      onSuccess();
      message.success(`Branch Link added successfully`);
      form.resetFields();
      onCancel();
    } catch (error) {
      if (error.message) message.error('Invalid data entry!');
    }
  };

  return (
    <Modal
      visible={modalVisible}
      title={'Create a new Link'}
      okText={'Submit'}
      cancelText="Cancel"
      onCancel={onCancel}
      onOk={handleSubmit}
    >
      <ProForm
        form={form}
        layout="vertical"
        name={`Create Link`}
        submitter={{
          render: (props, doms) => {
            return [];
          },
        }}
        initialValues={values}
      >
        <Row gutter={16}>
          <Col span={12}>
            <ProFormSelect
              name="from_branch"
              label="From"
              rules={[
                {
                  required: true,
                  message: 'You Must select an option',
                },
              ]}
              placeholder="Select option"
              request={getBranchesForDropdown}
            />
          </Col>

          <Col span={12}>
            <ProFormSelect
              name="to_branch"
              label="To"
              rules={[
                {
                  required: true,
                  message: 'You Must select an option',
                },
              ]}
              placeholder="Select option"
              request={getBranchesForDropdown}
            />
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <ProFormDigit
              rules={[
                {
                  required: true,
                  message: 'Must add value.',
                },
              ]}
              initialValue={1}
              label="Shipping Time (Days)"
              name="shipping_time"
            />
          </Col>

          <Col span={12}>
            <ProFormMoney
              rules={[
                {
                  required: true,
                  message: 'Must add value.',
                },
              ]}
              customSymbol="৳"
              label="Shipping Cost"
              name="shipping_cost"
            />
          </Col>
        </Row>
      </ProForm>
    </Modal>
  );
};

export default Form;
