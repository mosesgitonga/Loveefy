import React from 'react'
import { Helmet } from 'react-helmet'

function LandingIndex() {
  return (
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
  )
}

export default LandingIndex