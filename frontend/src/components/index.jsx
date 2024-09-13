import React from 'react';
import styles from './index.module.css';
import { useNavigate } from 'react-router-dom';

const IndexPage = () => {
    const navigate = useNavigate();

    return (
        <div>
            <header className={styles.headContainer}>
                <div className={styles.logoContainer}>
                    <h1>Loveefy</h1>
                    <p className={styles.tagline}>Find Love Through Career</p>
                </div>
                <nav>
                    <ul className={styles.navList}>
                        <li><a href='#hero'>Home</a></li>
                        <li><a href='#features'>Features</a></li>
                        <li><a href='#careers'>Careers</a></li>
                        <li><a href='#testimonials'>Testimonials</a></li>
                        <li><a href='#blog'>Blog</a></li>
                        <li><a href='#support'>Support</a></li>
                        <li><a href='#contact'>Contact</a></li>
                    </ul>
                </nav>
                <div className={styles.authButtons}>
                    <button className={styles.login} onClick={() => navigate('/login')}>Login</button>
                    <button className={styles.register} onClick={() => navigate('/register')}>Register</button>
                </div>
            </header>
            <main>
                <section id={styles.hero} className={styles.heroContainer}>
                    <div className={styles.heroContent}>
                        <h2>Find Love Through Career</h2>
                        <p>Join millions of singles and find your soulmate with Loveefy. Our advanced matching system connects you with professionals in your area who share your career ambitions and values.</p>
                        <button className={styles.ctaButton} onClick={() => navigate('/register')}>Join For Free</button>
                    </div>
                </section>

                <section id={styles.about} className={styles.aboutContainer}>
                    <h2>About Loveefy</h2>
                    <p>Loveefy is dedicated to creating meaningful connections by matching individuals based on career and location. Our platform is designed to help professionals find love without compromising their career goals. Learn more about our mission and values.</p>
                </section>

                <section id={styles.mission} className={styles.missionContainer}>
                    <h3>Our Mission</h3>
                    <p>At Loveefy, we aim to revolutionize dating by focusing on career-driven individuals. Our mission is to provide a platform where professionals can connect with like-minded people who understand and share their career ambitions.</p>
                </section>

                <section id={styles.careers} className={styles.careersContainer}>
                    <h2>Explore Careers</h2>
                    <p className={styles.careerIntro}>Discover professionals from various career paths who are looking for meaningful connections. Whether you're in tech, business, or healthcare, Loveefy helps you find a match that aligns with your career goals.</p>
                    <div className={styles.careers}>
                        <div className={styles.career}>
                            <img src="medics.jpg" alt="Medical Professionals" />
                            <h3>Medical Professionals</h3>
                            <p>Connect with doctors, nurses, and healthcare specialists who share your passion for medicine and patient care.</p>
                        </div>
                        <div className={styles.career}>
                            <img src="tech.avif" alt="Tech Professionals" />
                            <h3>Tech Innovators</h3>
                            <p>Meet software engineers, data scientists, and IT professionals who are driven by technology and innovation.</p>
                        </div>
                        <div className={styles.career}>
                            <img src="business professionals.jpeg" alt="Business Professionals" />
                            <h3>Business Leaders</h3>
                            <p>Find entrepreneurs, managers, and consultants who are focused on growing their careers and achieving success.</p>
                        </div>
                    </div>
                </section>

                <section id={styles.features} className={styles.featuresContainer}>
                    <h2>Why Choose Loveefy?</h2>
                    <div className={styles.features}>
                        <div className={styles.feature}>
                            <h3>Advanced Matching</h3>
                            <p>Our sophisticated algorithms analyze your career goals and location to provide you with the most compatible matches.</p>
                        </div>
                        <div className={styles.feature}>
                            <h3>User-Friendly Interface</h3>
                            <p>Enjoy a seamless and intuitive experience with our easy-to-navigate platform designed for professionals.</p>
                        </div>
                        <div className={styles.feature}>
                            <h3>Privacy & Security</h3>
                            <p>We prioritize your privacy and security, ensuring that your data is protected and your interactions are safe.</p>
                        </div>
                        <div className={styles.feature}>
                            <h3>Personalized Recommendations</h3>
                            <p>Receive tailored recommendations based on your career preferences and relationship goals.</p>
                        </div>
                    </div>
                </section>

                <section id={styles.testimonials} className={styles.testimonialsContainer}>
                    <h2>What Our Users Say</h2>
                    <div className={styles.testimonials}>
                        <div className={styles.testimonial}>
                            <p>"Loveefy helped me find my perfect match who shares my passion for technology and innovation. It's been an amazing experience!"</p>
                            <cite>- Emily, Software Engineer</cite>
                        </div>
                        <div className={styles.testimonial}>
                            <p>"I never thought I'd find someone who understands the demands of my medical career, but Loveefy made it possible."</p>
                            <cite>- Daniel, Surgeon</cite>
                        </div>
                        <div className={styles.testimonial}>
                            <p>"As a business professional, finding a partner who understands my career goals was important. Loveefy made that happen."</p>
                            <cite>- Sarah, Business Consultant</cite>
                        </div>
                    </div>
                </section>

                <section id={styles.blog} className={styles.blogContainer}>
                    <h2>Latest from Our Blog</h2>
                    <div className={styles.blogPosts}>
                        <article className={styles.blogPost}>
                            <h3><a href='/blog/1'>5 Tips for Balancing Career and Relationships</a></h3>
                            <p>Discover strategies for managing your career and personal life while building a meaningful relationship.</p>
                        </article>
                        <article className={styles.blogPost}>
                            <h3><a href='/blog/2'>The Importance of Career Compatibility in Relationships</a></h3>
                            <p>Learn why aligning your career goals with your partner's can lead to a more fulfilling relationship.</p>
                        </article>  

                        <article className={styles.blogPost}>
                            <h3><a href='/blog/3'>How to Use Loveefy to Find Your Ideal Partner</a></h3>
                            <p>Get tips on maximizing your Loveefy experience to find the perfect match based on your career and location.</p>
                        </article>
                    </div>
                </section>

                <section id={styles.support} className={styles.supportContainer}>
                    <h2>Customer Support</h2>
                    <p>Our dedicated support team is here to help you with any issues or questions you may have. We offer 24/7 assistance to ensure your experience with Loveefy is smooth and enjoyable.</p>
                    <button className={styles.supportButton} onClick={() => navigate('/support')}>Get Support</button>
                </section>

                <section id={styles.contact} className={styles.contactContainer}>
                    <h2>Contact Us</h2>
                    <p>If you have any inquiries or feedback, feel free to reach out to us. We're always here to help!</p>
                    <div className={styles.contactDetails}>
                        <p>Email: <a href="mailto:support@loveefy.com">support@loveefy.com</a></p>
                        <p>Phone: +2547 57 573 241</p>
                        <p>Address: Nairobi Kenya</p>
                    </div>
                </section>
            </main>
            <footer className={styles.footer}>
                <div className={styles.footerContent}>
                    <p>&copy; 2024 Loveefy. All rights reserved.</p>
                    <ul className={styles.footerNav}>
                        <li><a href='#about'>About</a></li>
                        <li><a href='#careers'>Careers</a></li>
                        <li><a href='#support'>Support</a></li>
                        <li><a href='#contact'>Contact</a></li>
                    </ul>
                </div>
            </footer>
        </div>
    );
};

export default IndexPage;