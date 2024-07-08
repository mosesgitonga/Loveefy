import React from 'react';
import styles from './index.module.css';
import { useNavigate } from 'react-router-dom'

const IndexPage = () => {
    const navigate = useNavigate()

    return (
        <div>
            <header className={styles.headContainer}>
                <h1>Loveefy</h1>
                <nav>
                    <ul>
                        <li><a href='#hero'>Hero</a></li>
                        <li><a href='#features'>Features</a></li>
                        <li><a href='#support'>Support</a></li>
                    </ul>
                </nav>
                <div className={styles.authButtons}>
                    <button className={styles.login} onClick={() => navigate('/login')}>Login</button>
                    <button className={styles.register} onClick={() => navigate('/register')}>Register</button>
                </div>
            </header>
            <main>
                <section id={styles.hero} className={styles.container}>
                    <div>
                        <h2>Find Love Through Career & Location</h2>
                        <p>Join millions of singles and find your soulmate</p>
                        <button className={styles.ctaButton} onClick={() => navigate('/register')}>Join For Free</button>
                    </div>

                </section>
                <div className={styles.mission}>
                    <h3>Our Mission</h3>
                    <p>Our dating site is designed to help you find love without sacrificing your career. Connect with professionals in your area who share your ambition and drive. Say goodbye to endless swiping and hello to meaningful connections that understand your lifestyle.</p>
                </div>
                <hr></hr>
                <p className={styles.careerP}>Find Your Soulmate In Your Preferred Career</p>
                <section className={styles.careers}>
                    <div className={styles.career}>
                        <img src="medics.jpg" alt="two medical practionals kissing" />
                        <h3>Medical practionals</h3>
                    </div>
                    <div className={styles.career}>
                        <img src="tech.avif" alt="" />
                        <h3>Tech</h3>
                    </div>
                    <div className={styles.career}>
                        <img src="education.avif" alt="" />
                        <h3>Engineering </h3>
                    </div>
                </section>
                <h2 className='featuresHeading'>Why Us?</h2>
                <section id={styles.features} className={styles.container}>
                    <div className={styles.feature}>
                        <h3>Advanced Matching</h3>
                        <p>Smart Algorithms to find the best matches for you</p>
                    </div>
                    <div className={styles.feature}>
                        <h3>Easy to use</h3>
                        <p>Intuitive design for seamless experience</p>
                    </div>
                    <div className={styles.feature}>
                        <h3>Secure</h3>
                        <p>Your privacy and safety are our number one priorities</p>
                    </div>
                </section>
            </main>
            <footer>
                <div className={styles.container}>
                    <p>&copy; 2024 Loveefy. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
}

export default IndexPage;
