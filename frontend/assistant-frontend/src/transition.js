import { motion } from "framer-motion";
import React from "react";
const transition = (OgComponent) => {
  const pageVariants = {
    initial: {
      opacity: 0,
      x: "-100vw",
    },
    in: {
      opacity: 1,
      x: 0,
    },
    out: {
      opacity: 0,
      x: "100vw",
    },
  };
  
  const pageTransition = {

    duration: 0.2,
  };
	return () =>  (
		<div>
			
			<motion.div
				initial="initial"
        animate="in"
        exit="out"
        variants={pageVariants}
        transition={pageTransition}
			><OgComponent /></motion.div>

		</div>
	);
};

export default transition;
