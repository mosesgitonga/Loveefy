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
                        <h2>Find Your Perfect Match</h2>
                        <p>Join millions of singles and find your soulmate</p>
                        <button className={styles.ctaButton} onClick={() => navigate('/register')}>Register</button>
                    </div>
                    <div className='heroImage'>
                        <img src='/images.jpeg' alt="lovers walking"/>
                    </div>
                </section>
                <h2 className='featuresHeading'>Our Features</h2>
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
