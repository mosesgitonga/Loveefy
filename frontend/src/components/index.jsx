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
                </div>
                <nav>
                    <ul className={styles.navList}>
                        <li><a href='#hero'>Home</a></li>
                        <li><a href='#features'>Features</a></li>
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
                        <h2>Find Love Through Career & Location</h2>
                        <p>Join millions of singles and find your soulmate</p>
                        <button className={styles.ctaButton} onClick={() => navigate('/register')}>Join For Free</button>
                    </div>
                </section>

                <section className={styles.missionContainer}>
                    <h3>Our Mission</h3>
                    <p>Loveefy is designed to help you find love without sacrificing your career. Connect with professionals in your area who share your ambition and drive.</p>
                </section>

                <section className={styles.careersContainer}>
                    <h2>Explore Careers</h2>
                    <p className={styles.careerIntro}>Find your soulmate in your preferred career path</p>
                    <div className={styles.careers}>
                        <div className={styles.career}>
                            <img src="medics.jpg" alt="Two medical practitioners kissing" />
                            <h3>Medical Professionals</h3>
                        </div>
                        <div className={styles.career}>
                            <img src="tech.avif" alt="Tech professionals" />
                            <h3>Tech</h3>
                        </div>
                        <div className={styles.career}>
                            <img src="engineering.jpg" alt="Engineers" />
                            <h3>Engineering</h3>
                        </div>
                    </div>
                </section>

                <section id={styles.features} className={styles.featuresContainer}>
                    <h2>Why Choose Loveefy?</h2>
                    <div className={styles.features}>
                        <div className={styles.feature}>
                            <h3>Advanced Matching</h3>
                            <p>Smart algorithms to find the best matches for you.</p>
                        </div>
                        <div className={styles.feature}>
                            <h3>Easy to Use</h3>
                            <p>Intuitive design for a seamless experience.</p>
                        </div>
                        <div className={styles.feature}>
                            <h3>Secure</h3>
                            <p>Your privacy and safety are our top priorities.</p>
                        </div>
                    </div>
                </section>

                <section id={styles.support} className={styles.supportContainer}>
                    <h2>Customer Support</h2>
                    <p>Need help? Our support team is here to assist you 24/7.</p>
                    <button className={styles.supportButton} onClick={() => navigate('/support')}>Get Support</button>
                </section>
            </main>
            <footer className={styles.footer}>
                <div className={styles.footerContent}>
                    <p>&copy; 2024 Loveefy. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default IndexPage;
