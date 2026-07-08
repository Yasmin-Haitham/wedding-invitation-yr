import { useEffect, useState } from 'react'
import petalA from '../assets/images/deco-flower-a.png'
import petalB from '../assets/images/deco-flower-b.png'
import styles from './Petals.module.css'

const PETAL_COUNT = 8
const PETAL_IMAGES = [petalA, petalB]

function makePetals() {
  return Array.from({ length: PETAL_COUNT }, (_, i) => ({
    id: i,
    src: PETAL_IMAGES[i % PETAL_IMAGES.length],
    left: Math.random() * 100,
    width: 14 + Math.random() * 12,
    duration: 9 + Math.random() * 8,
    delay: Math.random() * 6,
  }))
}

function Petals({ active }) {
  const [petals, setPetals] = useState([])

  useEffect(() => {
    if (active && petals.length === 0) {
      setPetals(makePetals())
    }
  }, [active, petals.length])

  if (!active || petals.length === 0) return null

  return (
    <>
      {petals.map((petal) => (
        <img
          key={petal.id}
          className={styles.petal}
          src={petal.src}
          alt=""
          style={{
            left: `${petal.left}vw`,
            width: `${petal.width}px`,
            animationDuration: `${petal.duration}s`,
            animationDelay: `${petal.delay}s`,
          }}
        />
      ))}
    </>
  )
}

export default Petals
