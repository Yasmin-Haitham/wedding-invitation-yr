import { motion, useReducedMotion } from 'framer-motion'
import envelopeImg from '../../assets/images/envelope.png'
import decoFlowerA from '../../assets/images/deco-flower-a.png'
import decoFlowerB from '../../assets/images/deco-flower-b.png'
import styles from './Envelope.module.css'

function Envelope({ onOpen }) {
  const reducedMotion = useReducedMotion()

  return (
    <motion.div
      className={styles.stage}
      exit={{ opacity: 0, scale: reducedMotion ? 1 : 0.9, y: reducedMotion ? 0 : 14 }}
      transition={{ duration: reducedMotion ? 0.2 : 0.7, ease: 'easeOut' }}
    >
      <div className={styles.scene}>
        <img className={`${styles.decoFlower} ${styles.tl}`} src={decoFlowerA} alt="" aria-hidden="true" />
        <img className={`${styles.decoFlower} ${styles.tr}`} src={decoFlowerA} alt="" aria-hidden="true" />
        <img className={`${styles.decoFlower} ${styles.bl}`} src={decoFlowerB} alt="" aria-hidden="true" />
        <img className={`${styles.decoFlower} ${styles.br}`} src={decoFlowerB} alt="" aria-hidden="true" />

        <motion.button
          className={styles.envelopeBtn}
          onClick={onOpen}
          whileHover={reducedMotion ? undefined : { y: -4 }}
          whileTap={reducedMotion ? undefined : { scale: 0.97 }}
        >
          <img src={envelopeImg} alt="A sealed cream envelope with a gold wax seal — tap to open the invitation" />
        </motion.button>
      </div>
      <p className={styles.hint}>tap to open</p>
    </motion.div>
  )
}

export default Envelope
