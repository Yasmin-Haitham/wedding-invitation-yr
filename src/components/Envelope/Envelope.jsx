import { useRef, useState } from 'react'
import { motion, useReducedMotion } from 'framer-motion'
import envelopeVideo from '../../assets/videos/Gen-4 Turbo - Overhead static macro shot of a luxury cream envelope with embossed floral scrollwork,.mp4'
import decoFlowerA from '../../assets/images/deco-flower-a.png'
import decoFlowerB from '../../assets/images/deco-flower-b.png'
import styles from './Envelope.module.css'

function Envelope({ onOpen }) {
  const reducedMotion = useReducedMotion()
  const videoRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)

  // Exit transition duration is 1.5s, so start fade out 1.5s before video ends.
  // For safety, if reducedMotion is enabled, we fade out in 0.2s, so we start 0.2s before the end.
  const fadeThreshold = reducedMotion ? 0.2 : 2.5

  const handleClick = () => {
    if (!isPlaying) {
      setIsPlaying(true)
      if (videoRef.current) {
        videoRef.current.play().catch((err) => {
          console.error('Failed to play video, opening immediately', err)
          onOpen()
        })
      }
    } else {
      // If already playing, a click skips and opens immediately
      onOpen()
    }
  }

  const handleTimeUpdate = (e) => {
    const video = e.currentTarget
    if (video.duration && video.currentTime >= video.duration - fadeThreshold) {
      onOpen()
    }
  }

  return (
    <motion.div
      className={styles.stage}
      exit={{ opacity: 0, scale: reducedMotion ? 1 : 0.9, y: reducedMotion ? 0 : 14 }}
      transition={{ duration: fadeThreshold, ease: 'easeOut' }}
    >
      <div className={styles.scene}>
        <img className={`${styles.decoFlower} ${styles.tl}`} src={decoFlowerA} alt="" aria-hidden="true" />
        <img className={`${styles.decoFlower} ${styles.tr}`} src={decoFlowerA} alt="" aria-hidden="true" />
        <img className={`${styles.decoFlower} ${styles.bl}`} src={decoFlowerB} alt="" aria-hidden="true" />
        <img className={`${styles.decoFlower} ${styles.br}`} src={decoFlowerB} alt="" aria-hidden="true" />

        <motion.button
          className={styles.envelopeBtn}
          onClick={handleClick}
          whileHover={reducedMotion ? undefined : { y: -4 }}
          whileTap={reducedMotion ? undefined : { scale: 0.97 }}
          aria-label="A sealed cream envelope with a gold wax seal — tap to open the invitation"
        >
          <div className={styles.videoCrop}>
            <video
              ref={videoRef}
              src={envelopeVideo}
              preload="auto"
              muted
              playsInline
              onTimeUpdate={handleTimeUpdate}
              onEnded={onOpen}
              className={styles.envelopeVideo}
            />
          </div>
        </motion.button>
      </div>
      <p
        className={styles.hint}
        style={{
          opacity: isPlaying ? 0 : undefined,
          transition: 'opacity 0.4s ease',
          pointerEvents: isPlaying ? 'none' : 'auto'
        }}
      >
        tap to open
      </p>
    </motion.div>
  )
}

export default Envelope
