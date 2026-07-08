import { motion, useReducedMotion } from 'framer-motion'
import decoFlowerA from '../assets/images/deco-flower-a.png'
import closingSealImg from '../assets/images/closing-seal.png'
import styles from './LetterContent.module.css'

function LetterContent({ visible }) {
  const reducedMotion = useReducedMotion()

  const container = {
    hidden: {},
    visible: { transition: { staggerChildren: reducedMotion ? 0 : 0.14 } },
  }

  const item = {
    hidden: { opacity: 0, y: reducedMotion ? 0 : 14 },
    visible: { opacity: 1, y: 0, transition: { duration: reducedMotion ? 0 : 0.8, ease: 'easeOut' } },
  }

  return (
    <motion.div
      className={styles.content}
      variants={container}
      initial="hidden"
      animate={visible ? 'visible' : 'hidden'}
    >
      <motion.p variants={item} className={styles.eyebrow}>
        together with their families
      </motion.p>

      <motion.h1 variants={item} className={styles.names}>
        Youssef <span className={styles.amp}>&amp;</span> Rowida
      </motion.h1>

      <motion.p variants={item} className={styles.inviteLine}>
        are inviting you to celebrate with them their wedding
      </motion.p>

      <motion.p variants={item} className={styles.welcomeMessage}>
        To our family and dearest friends — from every hello that led us here to this
        beautiful forever, you have been part of our story all along. We can hardly wait
        to hold your hands, share this joy, and begin our new chapter surrounded by the
        people we love most.
      </motion.p>

      <motion.div variants={item} className={styles.flowerDivider}>
        <span className={styles.line} />
        <img className={styles.flowerImg} src={decoFlowerA} alt="" />
        <span className={`${styles.line} ${styles.right}`} />
      </motion.div>

      <motion.div variants={item} className={styles.when}>
        <span className={styles.day}>wednesday</span>
        <span className={styles.dateMain}>
          July <span className={styles.num}>22</span>
        </span>
        <span className={styles.year}>2026</span>
      </motion.div>

      <motion.p variants={item} className={styles.timeLine}>
        7:00 PM
      </motion.p>

      <motion.div variants={item} className={styles.venue}>
        <p className={styles.venueLabel}>the venue</p>
        <p className={styles.venueName}>White Plaza Hall</p>
        <a
          className={styles.mapBtn}
          href="https://maps.app.goo.gl/AjYxmwDWQ9RRvFWu9?g_st=ic"
          target="_blank"
          rel="noopener"
        >
          <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z" />
          </svg>
          view location on maps
        </a>
      </motion.div>

      <motion.div variants={item} className={styles.closingSeal}>
        <img className={styles.closingSealImg} src={closingSealImg} alt="" />
        <p className={styles.closingText}>we can&apos;t wait to see you there</p>
      </motion.div>
    </motion.div>
  )
}

export default LetterContent
