import React from 'react';
import LandingIndex from './sections/LandingIndex';
import Footer from '../../components/common/Footer';
import LandingCareers from './sections/LandingCareers';
import LandingHero from './sections/LandingHero';
import Navbar from '../../components/common/Navbar';
import BlogList from '../Blog/BlogList';
import LandingAbout from './sections/LandingAbout'
import LandingChoose from './sections/LandingChoose'
import LandingTestimonial from './sections/LandingTestimonials'
import ContactSection from './sections/ContactSection'
import ContactSupport from './sections/ContactSupport'



const Landing = () => {

    return (
        <div>
            <LandingIndex />

            <Navbar />

            <main>
                <section id='hero' className='bg-white'>
                    <LandingHero />
                </section>

                <div id='about' className='bg-white'>
                    <LandingAbout />
                </div>
                

                <section id='careers' className="py-16 bg-gray-100">
                    <LandingCareers />
                </section>

                <section id='choose'>
                    <LandingChoose />
                </section>

                <section id='testimonials'>
                    <LandingTestimonial />
                </section>
                

                <section id="blog" className='md:mx-8 mx-3' >
                    <div className='md:py-32 py-16'>
                        <h2 className='md:mb-8'>Latest from Our Blog</h2>
                        <BlogList />
                    </div>
                </section>

                <section id='support' >
                    <ContactSupport />
                </section>

                <section id="contact" >
                    <ContactSection />
                </section>
            </main>

            <Footer />
        </div>
    );
};

export default Landing;