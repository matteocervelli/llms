// Fixture: known TSX violations for design-lint.sh tests
const styles = {
  fontFamily: "'Mona Sans', sans-serif",
};

const Hero = () => (
  <h1 style={{ WebkitBackgroundClip: "text" }}>
    -webkit-background-clip: text
  </h1>
);

export default Hero;
