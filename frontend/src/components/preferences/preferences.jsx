import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import Select from 'react-select';
import countries from 'i18n-iso-countries';
import enLocale from 'i18n-iso-countries/langs/en.json';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios.jsx';
import './PreferenceForm.css';

// Load country data for React Select
countries.registerLocale(enLocale);
const countryOptions = Object.entries(countries.getNames('en', { select: 'official' })).map(([value, label]) => ({
  value,
  label
}));

const validationSchema = Yup.object({
  gender: Yup.string().oneOf(['male', 'female', 'transgender', 'non-binary']).required('Required'),
  minAge: Yup.number().min(18, 'Minimum age is 18').required('Required'),
  maxAge: Yup.number().max(200, 'Maximum age is 200').required('Required').moreThan(Yup.ref('minAge'), 'Max age must be greater than min age'),
  country: Yup.string().required('Required'),
  region: Yup.string(),
  industryMajor: Yup.string().required('Required'),
  favHobby: Yup.string(),
  wantsChild: Yup.string().oneOf(['yes', 'no', 'not now']).required('Required')
});

const PreferenceForm = () => {
  const navigate = useNavigate();

  return (
    <div className='preference-window'>
      <h1>Loveefy</h1>
      <div className="preference-form">
        <h2>Preference Details</h2>
        <p>Please enter your preferences. Note: This is not your profile information.</p>

        <Formik
          initialValues={{
            gender: '',
            minAge: 18,
            maxAge: 100,
            country: '',
            region: '',
            industryMajor: '',
            favHobby: '',
            hasChild: '',
            wantsChild: ''
          }}
          validationSchema={validationSchema}
          onSubmit={async (values, { setSubmitting }) => {
            try {
              const response = await api.post('/v1/preferences', values);

              if (response.status === 201) {
                console.log('Profile created successfully');
                setSubmitting(false);
                navigate('/upload');
              } else {
                console.log('Unexpected status code:', response.status);
                setSubmitting(false);
              }
            } catch (error) {
              console.error('Error creating profile:', error);
              setSubmitting(false);
            }
          }}
        >
          {formik => (
            <Form onSubmit={formik.handleSubmit}>
              <div className="form-group">
                <label htmlFor="gender">Preferred Gender</label>
                <Field as="select" name="gender">
                  <option value="">Select the Gender You Prefer</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="transgender">Transgender</option>
                  <option value="non-binary">Non-binary</option>
                </Field>
                <ErrorMessage name="gender" component="div" className="error-message" />
              </div>

              <div className="age-range">
                <label>
                  Min Age: {formik.values.minAge}
                  <input
                    type="range"
                    name="minAge"
                    min="18"
                    max="100"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.minAge}
                  />
                  {formik.touched.minAge && formik.errors.minAge ? (
                    <div className="error">{formik.errors.minAge}</div>
                  ) : null}
                </label>
                <label>
                  Max Age: {formik.values.maxAge}
                  <input
                    type="range"
                    name="maxAge"
                    min="18"
                    max="100"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.maxAge}
                  />
                  {formik.touched.maxAge && formik.errors.maxAge ? (
                    <div className="error">{formik.errors.maxAge}</div>
                  ) : null}
                </label>
              </div>

              <div className="form-group">
                <label htmlFor="country">Country of Your Preferred Match</label>
                <Select
                  name="country"
                  options={countryOptions}
                  onChange={option => formik.setFieldValue('country', option.value)}
                  onBlur={formik.handleBlur}
                  value={countryOptions.find(option => option.value === formik.values.country)}
                />
                <ErrorMessage name="country" component="div" className="error-message" />
              </div>

              <div className="form-group">
                <label htmlFor="region">Preferred Partner Region (optional)</label>
                <Field
                  type="text"
                  name="region"
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  value={formik.values.region}
                />
                <ErrorMessage name="region" component="div" className="error-message" />
              </div>

              <div className="form-group">
                <label htmlFor="industryMajor">Preferred Partner Industry Major</label>
                <Field as="select" name="industryMajor">
                  <option value="">Select Preferred Partner Major</option>
                  <option value="health">Health</option>
                  <option value="finance">Finance</option>
                  <option value="it">IT</option>
                  <option value="agriculture">Agriculture</option>
                </Field>
                <ErrorMessage name="industryMajor" component="div" className="error-message" />
              </div>

              <div className="form-group">
                <label htmlFor="favHobby">Preferred Partner Favorite Hobby (optional)</label>
                <Field type="text" name="favHobby" />
                <ErrorMessage name="favHobby" component="div" className="error-message" />
              </div>


              <div className="form-group">
                <label htmlFor="wantsChild">Do You Want to have a child?</label>
                <Field as="select" name="wantsChild">
                  <option value="">Select an option</option>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                  <option value="not now">Not now, very soon</option>
                </Field>
                <ErrorMessage name="wantsChild" component="div" className="error-message" />
              </div>

              <button type="submit" disabled={formik.isSubmitting}>
                {formik.isSubmitting ? 'Submitting...' : 'Submit'}
              </button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default PreferenceForm;
