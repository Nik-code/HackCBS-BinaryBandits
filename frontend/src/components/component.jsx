'use client'

import { Button } from "@mui/material"
import { Card, CardContent } from "@mui/material"
import { BrainCircuit, MapPin, FileText, Bell, MessageCircle, TestTube, TrendingUp, Users } from "lucide-react"
import { motion } from "framer-motion"
import {Img} from "react-image"

export default function Component() {
  return (
    <div className="bg-neutral-50 min-h-screen">
      <header className="bg-white/80 backdrop-blur-sm fixed w-full z-50 shadow-sm">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            {/* <Image 
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/CuraNet_Logo-v2ODPLpANeEXfPECK6GjnRCoVodV4z.png"
              alt="CuraNet Logo"
              width={40}
              height={40}
              className="w-auto h-8"
            /> */}
            <span className="text-2xl font-bold text-teal-500">CuraNet</span>
          </div>
          <nav>
            <ul className="flex space-x-6">
              <li><a href="#features" className="text-neutral-600 hover:text-teal-500 transition-colors">Features</a></li>
              <li><a href="#community" className="text-neutral-600 hover:text-teal-500 transition-colors">Community</a></li>
              <li><a href="#cta" className="text-neutral-600 hover:text-teal-500 transition-colors">Get Started</a></li>
            </ul>
          </nav>
        </div>
      </header>

      <main>
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
          {/* Animated background elements */}
          <div className="absolute inset-0 z-0">
            <motion.div
              className="absolute top-1/4 left-1/4 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
              animate={{
                scale: [1, 1.2, 1],
                x: [0, 50, 0],
                y: [0, 30, 0],
              }}
              transition={{
                duration: 8,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
            <motion.div
              className="absolute top-1/3 right-1/4 w-96 h-96 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
              animate={{
                scale: [1.2, 1, 1.2],
                x: [0, -30, 0],
                y: [0, 50, 0],
              }}
              transition={{
                duration: 10,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
            <motion.div
              className="absolute bottom-1/4 left-1/3 w-80 h-80 bg-cyan-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
              animate={{
                scale: [1, 1.1, 1],
                x: [0, 40, 0],
                y: [0, -30, 0],
              }}
              transition={{
                duration: 9,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
          </div>

          {/* Hero content */}
          <div className="container mx-auto px-6 relative z-10 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-5xl font-bold text-neutral-800 mb-6">Welcome to CuraNet</h2>
              <p className="text-2xl text-neutral-600 mb-12">Your AI-Powered Healthcare Companion</p>
              <a href="/Login">
                <Button className="bg-teal-400 hover:bg-teal-500 text-white text-lg py-6 px-8">
                Get Started
                </Button>
              </a>
              
            </motion.div>
          </div>
        </section>

        <section id="features" className="py-24 bg-white/80 backdrop-blur-sm">
          <div className="container mx-auto px-6">
            <h2 className="text-4xl font-bold text-center text-neutral-800 mb-16">Key Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
              <FeatureCard
                icon={<BrainCircuit className="w-12 h-12 text-teal-400" />}
                title="AI Symptom Analysis"
                description="Get instant insights on your symptoms using advanced AI technology."
              />
              <FeatureCard
                icon={<MapPin className="w-12 h-12 text-teal-400" />}
                title="Nearby Healthcare"
                description="Find doctors and hospitals in your vicinity with ease."
              />
              <FeatureCard
                icon={<FileText className="w-12 h-12 text-teal-400" />}
                title="Report Analysis"
                description="AI-enhanced analysis of your medical reports for better understanding."
              />
              <FeatureCard
                icon={<Bell className="w-12 h-12 text-teal-400" />}
                title="Outbreak Alerts"
                description="Stay informed with real-time disease outbreak notifications."
              />
              <FeatureCard
                icon={<MessageCircle className="w-12 h-12 text-teal-400" />}
                title="Health Chatbot"
                description="Get instant health advice and recommendations from our AI chatbot."
              />
              <FeatureCard
                icon={<TestTube className="w-12 h-12 text-teal-400" />}
                title="Lab Test Recommendations"
                description="Receive personalized suggestions for relevant lab tests."
              />
              <FeatureCard
                icon={<TrendingUp className="w-12 h-12 text-teal-400" />}
                title="Health Trend Analysis"
                description="Visualize and understand trends in your medical history."
              />
              <FeatureCard
                icon={<Users className="w-12 h-12 text-teal-400" />}
                title="Community Support"
                description="Connect with others who have similar health conditions."
              />
            </div>
          </div>
        </section>

        <section id="community" className="py-24">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-4xl font-bold text-neutral-800 mb-8">Join Our Supportive Community</h2>
            <p className="text-xl text-neutral-600 mb-12">
              Connect with others, share experiences, and find support in your healthcare journey.
            </p>
            <Button className="bg-teal-400 hover:bg-teal-500 text-white text-lg py-6 px-8">Join Community</Button>
          </div>
        </section>

        <section id="cta" className="py-24 bg-gradient-to-r from-teal-400 to-emerald-400 text-white">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-4xl font-bold mb-8">Ready to Take Control of Your Health?</h2>
            <p className="text-xl mb-12">
              Start your journey towards better health management with CuraNet today.
            </p>
            <Button className="bg-white text-teal-500 hover:bg-neutral-100 text-lg py-6 px-8">Download CuraNet</Button>
          </div>
        </section>
      </main>

      <footer className="py-12 text-neutral-600">
        <div className="container mx-auto px-6 text-center">
          <div className="flex justify-center items-center gap-2 mb-4">
            <Img
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/CuraNet_Logo-v2ODPLpANeEXfPECK6GjnRCoVodV4z.png"
              alt="CuraNet Logo"
              width={30}
              height={30}
              className="w-auto h-6"
            />
            <span className="text-lg font-semibold text-teal-500">CuraNet</span>
          </div>
          <p>&copy; 2023 CuraNet. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description }) {
  return (
    <Card className="border-none shadow-none">
      <CardContent className="p-6 text-center">
        <div className="mb-6 flex justify-center">{icon}</div>
        <h3 className="text-xl font-semibold text-neutral-800 mb-4">{title}</h3>
        <p className="text-neutral-600">{description}</p>
      </CardContent>
    </Card>
  )
}