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
    <div className="preference-window">
      <div className="preference-form-container">
        <h1 className="title">Loveefy</h1>
        <div className="preference-form">
          <h2 className="form-title">Preference Details</h2>
          <p className="form-description">Please enter your preferences. Note: This is not your profile information.</p>

          <Formik
            initialValues={{
              gender: '',
              minAge: 18,
              maxAge: 100,
              country: '',
              region: '',
              industryMajor: '',
              career: '',
              education_level: '',
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
                <div className="form-row">
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

                  <div className="form-group">
                    <label>Age Range</label>
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
                        <ErrorMessage name="minAge" component="div" className="error-message" />
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
                        <ErrorMessage name="maxAge" component="div" className="error-message" />
                      </label>
                    </div>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="country">Country of Your Preferred Match</label>
                    <Select
                      name="country"
                      options={countryOptions}
                      onChange={option => formik.setFieldValue('country', option.value)}
                      onBlur={formik.handleBlur}
                      value={countryOptions.find(option => option.value === formik.values.country)}
                      className="react-select"
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
                      className="text-input"
                    />
                    <ErrorMessage name="region" component="div" className="error-message" />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="is_schooling">Preferred Education Status</label>
                    <Field as="select" name="is_schooling">
                      <option value="">Select an option</option>
                      <option value="yes">Schooling</option>
                      <option value="no">Graduated</option>
                      <option value="any">Any</option>
                    </Field>
                    <ErrorMessage name="is_schooling" component="div" className="error-message" />
                  </div>

                  <div className="form-group">
                    <label htmlFor="industryMajor">Preferred Partner Industry Major</label>
                    <Field as="select" name="industryMajor">
                      <option value="" label="Select industry major" />
                      <option value="health" label="Health" />
                      <option value="it" label="IT" />
                      <option value="finance" label="Finance" />
                      <option value="law" label="Law" />
                      <option value="engineering" label="Engineering" />
                      <option value="education" label="Education" />
                      <option value="scientific_research" label="Scientific Research" />
                      <option value="manufacturing" label="Manufacturing" />
                      <option value="retail" label="Retail" />
                      <option value="transportation" label="Transportation" />
                      <option value="agriculture" label="Agriculture" />
                      <option value="hospitality" label="Hospitality" />
                      <option value="construction" label="Construction" />
                      <option value="real_estate" label="Real Estate" />
                      <option value="security" label="Security" />
                      <option value="others" label="Others" />
                    </Field>
                    <ErrorMessage name="industryMajor" component="div" className="error-message" />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="career">Preferred Partner Profession</label>
                    <Field
                      type="text"
                      name="career"
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                      value={formik.values.career}
                      className="text-input"
                    />
                    <ErrorMessage name="career" component="div" className="error-message" />
                  </div>

                  <div className="form-group">
                    <label htmlFor="education_level">Preferred Partner Education Level</label>
                    <Field as="select" name="education_level">
                      <option value="">Select Preferred Partner Education Level</option>
                      <option value="primary">Primary Education</option>
                      <option value="secondary">Secondary Education</option>
                      <option value="post-secondary">Post-Secondary (Masters, Degree, Diploma, Cert)</option>
                      <option value="Doctoral">Doctoral (PhD)</option>
                    </Field>
                    <ErrorMessage name="education_level" component="div" className="error-message" />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="employment">Employment</label>
                    <Field as="select" name="employment">
                      <option value="">I want my match to be: </option>
                      <option value="employed">Employed</option>
                      <option value="unemployed">Unemployed</option>
                      <option value="self-employed">Self Employed</option>
                      <option value="entrepreneur">Entrepreneur</option>
                    </Field>
                    <ErrorMessage name="employment" component="div" className="error-message" />
                  </div>

                  <div className="form-group">
                    <label htmlFor="favHobby">Preferred Partner Favorite Hobby (optional)</label>
                    <Field
                      type="text"
                      name="favHobby"
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                      value={formik.values.favHobby}
                      className="text-input"
                    />
                    <ErrorMessage name="favHobby" component="div" className="error-message" />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="hasChild">I Prefer a Match With Children</label>
                    <Field as="select" name="hasChild">
                      <option value="">Select Preferred Match Status</option>
                      <option value="yes">Yes</option>
                      <option value="no">No</option>
                      <option value="does not matter">Doesn't Matter</option>
                    </Field>
                    <ErrorMessage name="hasChild" component="div" className="error-message" />
                  </div>

                  <div className="form-group">
                    <label htmlFor="wantsChild">Want Children?</label>
                    <Field as="select" name="wantsChild">
                      <option value="">Select Match's Preference</option>
                      <option value="yes">Yes</option>
                      <option value="no">No</option>
                      <option value="not now">Not now</option>
                    </Field>
                    <ErrorMessage name="wantsChild" component="div" className="error-message" />
                  </div>
                </div>

                <button type="submit" className="submit-button">Next</button>
              </Form>
            )}
          </Formik>
        </div>
      </div>
    </div>
  );
};

export default PreferenceForm;
