import { useEffect, useRef, useState } from 'react'
import { motion, useReducedMotion } from 'framer-motion'
import emblemTopImg from '../../assets/images/emblem-top.png'
import emblemBottomImg from '../../assets/images/emblem-bottom.png'
import flourishImg from '../../assets/images/flourish.png'
import LetterContent from '../LetterContent.jsx'
import styles from './Letter.module.css'

const COLLAPSED_HEIGHT = 112

function Letter({ isOpen, contentVisible, onUnfolded }) {
  const reducedMotion = useReducedMotion()
  const contentRef = useRef(null)
  const [expandedHeight, setExpandedHeight] = useState(COLLAPSED_HEIGHT)

  useEffect(() => {
    function measure() {
      if (contentRef.current) setExpandedHeight(contentRef.current.scrollHeight)
    }
    measure()
    window.addEventListener('resize', measure)
    return () => window.removeEventListener('resize', measure)
  }, [])

  return (
    <motion.main
      className={styles.stage}
      aria-hidden={!isOpen}
      animate={{ opacity: isOpen ? 1 : 0 }}
      transition={{ duration: reducedMotion ? 0.01 : 0.6 }}
    >
      <motion.div
        className={styles.frame}
        animate={{ height: isOpen ? expandedHeight : COLLAPSED_HEIGHT }}
        transition={
          reducedMotion
            ? { duration: 0.01 }
            : { duration: 1.15, ease: [0.65, 0, 0.32, 1], delay: isOpen ? 0.15 : 0 }
        }
        onAnimationComplete={() => {
          if (isOpen) onUnfolded()
        }}
      >
        <div className={styles.letter} ref={contentRef}>
          <img className={styles.emblemTop} src={emblemTopImg} alt="" aria-hidden="true" />
          <img className={styles.emblemBottom} src={emblemBottomImg} alt="" aria-hidden="true" />
          <img className={`${styles.flourish} ${styles.tl}`} src={flourishImg} alt="" aria-hidden="true" />
          <img className={`${styles.flourish} ${styles.tr}`} src={flourishImg} alt="" aria-hidden="true" />
          <img className={`${styles.flourish} ${styles.bl}`} src={flourishImg} alt="" aria-hidden="true" />
          <img className={`${styles.flourish} ${styles.br}`} src={flourishImg} alt="" aria-hidden="true" />

          <div
            className={`${styles.crease} ${styles.crease1}`}
            style={{ opacity: isOpen || reducedMotion ? 0 : 1 }}
          />
          <div
            className={`${styles.crease} ${styles.crease2}`}
            style={{ opacity: isOpen || reducedMotion ? 0 : 1 }}
          />

          <LetterContent visible={contentVisible} />
        </div>
      </motion.div>
    </motion.main>
  )
}

export default Letter
