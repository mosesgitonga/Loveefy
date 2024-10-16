import React from 'react';
import styles from './index.module.css';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet';

const IndexPage = () => {
    const navigate = useNavigate();

    return (
        <div>
            <Helmet>
                {/* Primary Meta Tags */}
                <title>Loveefy - Find Love Through Career</title>

                {/* Favicon Links */}
                <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
                <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
                <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
                <link rel="manifest" href="/site.webmanifest" />
                <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5" />
                <meta name="msapplication-TileColor" content="#da532c" />
                <meta name="theme-color" content="#ffffff" />

                {/* seo */}
                <meta name="description" content="Find love with professionals who share your career ambitions. Join millions of singles in Nairobi on Loveefy, Kenya's career-driven dating platform." />
                <meta name="keywords" content="dating, career dating, professional matchmaking, career, love, relationships, Nairobi, Kenya, career dating, free dating site, best dating site, dating app" />
                <meta name="author" content="Loveefy Team" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />

                {/* Open Graph / Facebook */}
                <meta property="og:title" content="Loveefy - Find Love Through Career" />
                <meta property="og:description" content="Find your soulmate with Loveefy, the dating platform for career-driven individuals in Nairobi, Kenya." />
                <meta property="og:image" content="https://loveefy.africa/uploads/1j+ojFVDOMkX9Wytexe43D6kh...6CrRRKmhrJwXs1M3EMoAJtlyIqhfBt8f85" />
                <meta property="og:image:alt" content="Loveefy - Find Love Through Career" />
                <meta property="og:url" content="https://www.loveefy.africa" />
                <meta property="og:type" content="website" />
                <meta property="og:locale" content="en_KE" />


                {/* Twitter */}
                <meta name="twitter:card" content="summary_large_image" />
                <meta name="twitter:title" content="Loveefy - Find Love Through Career" />
                <meta name="twitter:description" content="Join millions of singles in Nairobi, Kenya, and find your soulmate with Loveefy. Our platform connects professionals who share your career ambitions." />
                <meta name="twitter:image" content="https://loveefy.africa/uploads/1j+ojFVDOMkX9Wytexe43D6kh...6CrRRKmhrJwXs1M3EMoAJtlyIqhfBt8f85" />

                {/* Canonical and hreflang Links for SEO */}
                <link rel="canonical" href="https://www.loveefy.africa" />
                <link rel="alternate" href="https://www.loveefy.africa" hreflang="en-ke" />
                <link rel="alternate" href="https://www.loveefy.africa/sw" hreflang="sw-ke" />

                {/* Preconnect and Prefetch */}
                <link rel="preconnect" href="https://www.loveefy.africa" />
                <link rel="dns-prefetch" href="https://www.loveefy.africa" />
                
                {/* Structured Data for Organization */}
                <script type="application/ld+json">
                    {JSON.stringify({
                        "@context": "https://schema.org",
                        "@type": "Organization",
                        "name": "Loveefy",
                        "url": "https://www.loveefy.africa",
                        "logo": "https://www.loveefy.africa/images/logo.png",
                        "sameAs": [
                            "https://web.facebook.com/profile.php?id=61566381123254",
                            "https://x.com/LoveefyDating"
                        ],
                        "contactPoint": {
                            "@type": "ContactPoint",
                            "telephone": "+254757573241",
                            "contactType": "Customer Support",
                            "areaServed": "KE",
                            "availableLanguage": ["English", "Swahili"]
                        },
                        "address": {
                            "@type": "PostalAddress",
                            "streetAddress": "Kasarani, Nairobi",
                            "addressLocality": "Nairobi",
                            "addressRegion": "Nairobi",
                            "postalCode": "00100",
                            "addressCountry": "KE"
                        },
                        "foundingDate": "2005-6-6"
                    })}
                </script>

                {/* Structured Data for FAQ Page */}
                <script type="application/ld+json">
                    {JSON.stringify({
                        "@context": "https://schema.org",
                        "@type": "FAQPage",
                        "mainEntity": [{
                            "@type": "Question",
                            "name": "How does Loveefy work?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "Loveefy connects professionals based on their career ambitions. Create a profile, set your preferences, and start finding matches."
                            }
                        }, {
                            "@type": "Question",
                            "name": "Is Loveefy free?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "Yes, Loveefy is completely free. Free to send messages to anyone after you have matched."
                            }
                        }, {
                            "@type": "Question",
                            "name": "Does Loveefy contain ads?",
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": "No, Loveefy is completely free of ads. We prioritize smooth user experience for everyone."
                            }
                        }]
                    })}
                </script>

                {/* WebPage Structured Data */}
                <script type="application/ld+json">
                    {JSON.stringify({
                        "@context": "https://schema.org",
                        "@type": "WebPage",
                        "name": "Loveefy - Find Love Through Career",
                        "description": "Join millions of singles in Nairobi, Kenya, and find your soulmate with Loveefy. Our platform connects professionals who share your career ambitions.",
                        "url": "https://www.loveefy.africa",
                        "inLanguage": ["en", "sw"],
                        "isPartOf": {
                            "@type": "WebSite",
                            "url": "https://www.loveefy.africa"
                        },
                        "potentialAction": {
                            "@type": "SearchAction",
                            "target": "https://www.loveefy.africa/search?query={search_term_string}",
                            "query-input": "required name=search_term_string"
                        }
                    })}
                </script>
            </Helmet>



            <header className={styles.headContainer}>
                <div className={styles.logoContainer}>
                    <img className="logoImage" src="/loveefy.png" alt="Loveefy" />
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
                            <img src="business.jpeg" alt="Business Professionals" />
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